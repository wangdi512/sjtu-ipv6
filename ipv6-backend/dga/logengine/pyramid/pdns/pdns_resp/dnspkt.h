#ifndef __DNSPKT_H_
#define __DNSPKT_H_

#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <endian.h>
#include <arpa/inet.h>
#include <ldns/ldns.h>
#include "dnsfile.h"

typedef struct {
    uint8_t ipver;
    uint32_t ip4;
    uint64_t ip6h;
    uint64_t ip6l;
    uint16_t port;
} host_t;

void __print_ts (FILE *output, struct timeval ts) {
    struct tm *ts_tm = localtime(&(ts.tv_sec));
    char str_time[24];
    strftime(str_time, sizeof str_time, "%Y-%m-%d %H:%M:%S", ts_tm);
    fprintf(output, "%s\t", str_time);
}

void __print_ip (FILE *output, host_t *host) {
    if (host->ipver == 4) {
        struct in_addr addr;
        addr.s_addr = htobe32(host->ip4);
        fprintf(output, "%s\t", inet_ntoa(addr));
    } else if (host->ipver == 6) {
        fprintf(output, "%016llX%016llX\t", (unsigned long long)(host->ip6h), (unsigned long long)(host->ip6l));
    } else {
        fprintf(output, "\t");
    }
}

void dnspkt_printresp (ldns_pkt *pkt, struct timeval ts, host_t *src, host_t *dst) {
    FILE *output = dnsfile_resp();
    __print_ts(output, ts);
    __print_ip(output, src);
    __print_ip(output, dst);
    fprintf(output, "%u\t", (uint16_t)ldns_pkt_size(pkt));
    fprintf(output, "%u\t", ldns_pkt_aa(pkt));
    fprintf(output, "%u\t", ldns_pkt_tc(pkt));
    fprintf(output, "%u\t", ldns_pkt_rd(pkt));
    fprintf(output, "%u\t", ldns_pkt_ra(pkt));
    fprintf(output, "%u\t", ldns_pkt_get_rcode(pkt));
    fprintf(output, "%u\t", ldns_pkt_qdcount(pkt));
    fprintf(output, "%u\t", ldns_pkt_ancount(pkt));
    fprintf(output, "%u\t", ldns_pkt_nscount(pkt));
    fprintf(output, "%u\t", ldns_pkt_arcount(pkt));
    ldns_rr_list *rrlist = ldns_pkt_question(pkt);
    if (ldns_rr_list_rr_count(rrlist) > 0) {
        ldns_rr_print(output, ldns_rr_list_rr(rrlist, 0));
    } else {
        fprintf(output, "\t\t\n");
    }
}

void dnspkt_proc (const char *bytes, uint16_t len, struct timeval ts, host_t *src, host_t *dst) {
    
    ldns_pkt *pkt;
    if (ldns_wire2pkt(&pkt, bytes, len) != LDNS_STATUS_OK) {
        return;
    }
    
    if (ldns_pkt_get_opcode(pkt) != LDNS_PACKET_QUERY) goto done;
    
    uint16_t i;
    ldns_rr_list *rrlist;
    
    if (ldns_pkt_qr(pkt) == 1) {
        dnspkt_printresp(pkt, ts, src, dst);
    }
    
done:
    ldns_pkt_free(pkt);
    
}

#endif //__DNSPKT_H_
