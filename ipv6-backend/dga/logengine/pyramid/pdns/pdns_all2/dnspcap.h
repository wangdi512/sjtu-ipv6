#ifndef __DNSPCAP_H_
#define __DNSPCAP_H_

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <endian.h>
#include <pcap.h>
#include "dnspkt.h"

void dnspcap_pkt (unsigned char *arg, const struct pcap_pkthdr *pkthdr, const unsigned char *bytes) {
    
    // Check minimum packet size
    // 14 (Ethernet) + 20 (IPv4) + 8 (UDP) + 12 (DNS) = 54
    if (pkthdr->len < 54) { 
        return;
    }
    
    host_t src;
    host_t dst;
    memset(&src, 0, sizeof(host_t));
    memset(&src, 0, sizeof(host_t));
    
    // Ethernet Header
    uint16_t i = 12;
    while ((bytes[i + 1] == 0x00 && (bytes[i] == 0x81 || bytes[i] == 0x91
                                     || bytes[i] == 0x92 || bytes[i] == 0x93))
           || (bytes[i] == 0x88 && bytes[i + 1] == 0xa8)) {
        // VLAN tagging
        // EtherType = 0x8100, 0x9100, 0x9200, 0x9300, 0x88a8
        i += 4;
    }
    
    // IP Header
    if (bytes[i] == 0x08 && bytes[i + 1] == 0x00) {
        // IPv4
        i += 2;
        if ((bytes[i] & 0xF0) != 0x40) // Require: version = 4
            return;
        if (bytes[i + 9] != 17) // Require: protocol = 17 (UDP)
            return;
        src.ipver = 4;
        src.ip4 = be32toh(*(uint32_t *)&bytes[i + 12]);
        dst.ipver = 4;
        dst.ip4 = be32toh(*(uint32_t *)&bytes[i + 16]);
        i += (bytes[i] & 0x0F) << 2; // IHL
    } else if (bytes[i] == 0x86 && bytes[i + 1] == 0xDD) {
        // IPv6
        i += 2;
        if ((bytes[i] & 0xF0) != 0x60) // Require: version = 6
            return;
        /* TODO: IPv6 Extension Headers? */
        if (bytes[i + 6] != 17) // Require: next header = 17 (UDP)
            return;
        src.ipver = 6;
        src.ip6h = be64toh(*(uint64_t *)&bytes[i + 8]);
        src.ip6l = be64toh(*(uint64_t *)&bytes[i + 16]);
        dst.ipver = 6;
        dst.ip6h = be64toh(*(uint64_t *)&bytes[i + 24]);
        dst.ip6l = be64toh(*(uint64_t *)&bytes[i + 32]);
        i += 40;
    }
    
    // UDP Header
    src.port = be16toh(*((uint16_t *)(bytes + i)));
    dst.port = be16toh(*((uint16_t *)(bytes + i + 2)));
    i += 8;
    
    // Calculate DNS packet length
    uint16_t dnslen = pkthdr->len - i;
    if (dnslen < 12) {
        return;
    }
    
    // Process the DNS packet
    dnspkt_proc((char *)(bytes + i), dnslen, pkthdr->ts, &src, &dst);
    
}

void dnspcap_start (char *dev) {

    char errbuf[PCAP_ERRBUF_SIZE];
    
    if (dev == NULL) {
        // Use default device
        dev = pcap_lookupdev(errbuf);
        if (dev == NULL) {
            fprintf(stderr, "Error: cannot get default device: %s\n", errbuf);
            exit(1);
        }
    }
    
    printf("Opening device %s...\n", dev);
    
    pcap_t *handle;
    handle = pcap_open_live(dev, 65535, 1, 1000, errbuf);
    
    if (handle == NULL) {
        handle = pcap_open_offline(dev, errbuf);
        if (handle == NULL) {
            fprintf(stderr, "Error: cannot open device %s: %s\n", dev, errbuf);
            exit(1);
        }
    }
    
    struct bpf_program fp;
    char filter_exp[] = "udp port 53";
    
    bpf_u_int32 net;
    bpf_u_int32 mask;
    if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
        fprintf(stderr, "Error: cannot get netmask for device %s: %s\n", dev, errbuf);
        net = 0;
        mask = 0;
    }
    if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1) {
        fprintf(stderr, "Error: cannot compile pcap filter %s: %s\n", filter_exp, pcap_geterr(handle));
        exit(1);
    }
    if (pcap_setfilter(handle, &fp) == -1) {
        fprintf(stderr, "Error: cannot set pcap filter %s: %s\n", filter_exp, pcap_geterr(handle));
        exit(1);
    }
    
    pcap_loop(handle, -1, dnspcap_pkt, NULL);
    
}

#endif //__DNSPCAP_H_

