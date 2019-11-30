#ifndef __DNSPKT_H_
#define __DNSPKT_H_

#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <endian.h>
#include <arpa/inet.h>
#include <ldns/ldns.h>
#include "dnsfile.h"
#include "dnscache.h"

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

void __sprint_ip (char *output, host_t *host) {
    if (host->ipver == 4) {
        struct in_addr addr;
        addr.s_addr = htobe32(host->ip4);
        sprintf(output, "%s\t", inet_ntoa(addr));
    } else if (host->ipver == 6) {
        sprintf(output, "%016llX%016llX\t", (unsigned long long)(host->ip6h), (unsigned long long)(host->ip6l));
    } else {
        sprintf(output, "\t");
    }
}

void dnspkt_printrr (ldns_rr *rr, struct timeval ts, host_t *src, host_t *dst, uint16_t section) {
    
    char *rrstr = ldns_rr2str(rr);
    if (rrstr == NULL) return;
    char *data = (char *)malloc(strlen(rrstr) + 100);
    if (data == NULL) {
        free(rrstr);
        return;
    }
    
    char srcip[64];
    __sprint_ip(srcip, src);
    
    if (section == 0) {
        sprintf(data, "%sAN\t%s", srcip, rrstr);
    } else if (section == 1) {
        sprintf(data, "%sNS\t%s", srcip, rrstr);
    } else if (section == 2) {
        sprintf(data, "%sAR\t%s", srcip, rrstr);
    } else {
        sprintf(data, "%s\t%s", srcip, rrstr);
    }
    free(rrstr);
    
    if (dnscache_rr(data) == false) {
        FILE *output = dnsfile_rr();
        __print_ts(output, ts);
        fprintf(output, "%s", data);
    }
    
    free(data);
    
}

void dnspkt_proc (const char *bytes, uint16_t len, struct timeval ts, host_t *src, host_t *dst) {
    
    ldns_pkt *pkt;
    if (ldns_wire2pkt(&pkt, (const uint8_t *)bytes, len) != LDNS_STATUS_OK) {
        return;
    }
    
    if (ldns_pkt_qr(pkt) == 0) goto done;
    if (ldns_pkt_get_opcode(pkt) != LDNS_PACKET_QUERY) goto done;
    if (ldns_pkt_aa(pkt) == 0) goto done;
    if (ldns_pkt_tc(pkt) == 1) goto done;
    if (ldns_pkt_rd(pkt) == 1) goto done;
    if (ldns_pkt_get_rcode(pkt) != LDNS_RCODE_NOERROR) goto done;
    
    uint16_t i;
    ldns_rr_list *rrlist;
    
    rrlist = ldns_pkt_answer(pkt);
    for (i = 0; i < ldns_rr_list_rr_count(rrlist); i++) {
        dnspkt_printrr(ldns_rr_list_rr(rrlist, i), ts, src, dst, 0);
    }
    rrlist = ldns_pkt_authority(pkt);
    for (i = 0; i < ldns_rr_list_rr_count(rrlist); i++) {
        dnspkt_printrr(ldns_rr_list_rr(rrlist, i), ts, src, dst, 1);
    }
    rrlist = ldns_pkt_additional(pkt);
    for (i = 0; i < ldns_rr_list_rr_count(rrlist); i++) {
        dnspkt_printrr(ldns_rr_list_rr(rrlist, i), ts, src, dst, 2);
    }
    
done:
    ldns_pkt_free(pkt);
    
}

#endif //__DNSPKT_H_
