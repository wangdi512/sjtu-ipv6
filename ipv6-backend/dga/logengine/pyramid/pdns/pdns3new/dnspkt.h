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

#include "dnsenv.h"

inline void __print_ts (FILE *output, struct timeval ts) {
    struct tm *ts_tm = localtime(&(ts.tv_sec));
    char str_time[24];
    strftime(str_time, sizeof str_time, "%Y-%m-%d %H:%M:%S", ts_tm);
    fprintf(output, "%s", str_time);
}

inline void __print_ip (FILE *output, host_t *host) {
    if (host->ipver == 4) {
        struct in_addr addr;
        addr.s_addr = htobe32(host->ip4);
        fprintf(output, "%s", inet_ntoa(addr));
    } else if (host->ipver == 6) {
        fprintf(output, "%016llX%016llX", (unsigned long long)(host->ip6h), (unsigned long long)(host->ip6l));
    }
}

void dnspkt_tun (ldns_pkt *pkt, struct timeval ts, host_t *dst) {
    // require: response, rcode = noerror / nxdomain, qclass = in, ancount > 0
    // ts, client, msglen, rcode, ancount, ansize, qname, qtype
    
    if (ldns_pkt_get_rcode(pkt) != LDNS_RCODE_NOERROR &&
            ldns_pkt_get_rcode(pkt) != LDNS_RCODE_NXDOMAIN) {
        return;
    }
    if (ldns_pkt_ancount(pkt) == 0) {
        return;
    }
    
    ldns_rr_list *qlist;
    ldns_rr *q;
    qlist = ldns_pkt_question(pkt);
    if (ldns_rr_list_rr_count(qlist) == 0) {
        return;
    }
    q = ldns_rr_list_rr(qlist, 0);
    if (ldns_rr_get_class(q) != LDNS_RR_CLASS_IN) {
        return;
    }
    
    ldns_rr_list *rrlist;
    ldns_rr *rr;
    rrlist = ldns_pkt_answer(pkt);
    size_t ansize = 0;
    size_t i, j;
    for (i = 0; i < ldns_rr_list_rr_count(rrlist); i++) {
        rr = ldns_rr_list_rr(rrlist, i);
        for (j = 0; j < ldns_rr_rd_count(rr); j++) {
            ansize += ldns_rdf_size(ldns_rr_rdf(rr, j));
        }
    }
    
    FILE *output = dnsfile_tun();
    
    __print_ts(output, ts);
    fprintf(output, "\t");
    __print_ip(output, dst);
    fprintf(output, "\t");
    fprintf(output, "%zu\t", ldns_pkt_size(pkt));
    fprintf(output, "%u\t", ldns_pkt_get_rcode(pkt));
    fprintf(output, "%u\t", ldns_pkt_ancount(pkt));
    fprintf(output, "%zu\t", ansize);
    ldns_rdf_print(output, ldns_rr_owner(q));
    fprintf(output, "\t");
    fprintf(output, "%u", ldns_rr_get_type(q));
    fprintf(output, "\n");
    
    
}

void dnspkt_dga (ldns_pkt *pkt, struct timeval ts, host_t *dst) {
    // require: response, rcode = nxdomain, qclass = in, qtype = a
    // ts, client, qname
    
    if (ldns_pkt_get_rcode(pkt) != LDNS_RCODE_NXDOMAIN) {
        return;
    }
    
    ldns_rr_list *qlist;
    ldns_rr *q;
    
    qlist = ldns_pkt_question(pkt);
    if (ldns_rr_list_rr_count(qlist) == 0) {
        return;
    }
    q = ldns_rr_list_rr(qlist, 0);
    
    if (ldns_rr_get_class(q) != LDNS_RR_CLASS_IN) {
        return;
    }
    if (ldns_rr_get_type(q) != LDNS_RR_TYPE_A) {
        return;
    }
    
    FILE *output = dnsfile_dga();
    
    __print_ts(output, ts);
    fprintf(output, "\t");
    __print_ip(output, dst);
    fprintf(output, "\t");
    ldns_rdf_print(output, ldns_rr_owner(q));
    fprintf(output, "\n");
}

void dnspkt_flux (ldns_pkt *pkt, struct timeval ts) {
    // require: response, rd = 0, aa = 1, rcode = noerror, qclass = in, qtype = a, ancount > 0
    // ts, qname, a-ip-list
    
/*    if (ldns_pkt_rd(pkt) != 0 || ldns_pkt_aa(pkt) != 1) {
        return;
    }
*/
    if (ldns_pkt_get_rcode(pkt) != LDNS_RCODE_NOERROR) {
        return;
    }
    if (ldns_pkt_ancount(pkt) == 0) {
        return;
    }
    
    ldns_rr_list *qlist;
    ldns_rr *q;
    qlist = ldns_pkt_question(pkt);
    if (ldns_rr_list_rr_count(qlist) == 0) {
        return;
    }
    q = ldns_rr_list_rr(qlist, 0);
    if (ldns_rr_get_class(q) != LDNS_RR_CLASS_IN) {
        return;
    }
    if (ldns_rr_get_type(q) != LDNS_RR_TYPE_A) {
        return;
    }
    
    FILE *output;
    
    ldns_rr_list *rrlist;
    ldns_rr *rr;
    rrlist = ldns_pkt_answer(pkt);
    size_t i;
    bool printing = false;
    for (i = 0; i < ldns_rr_list_rr_count(rrlist); i++) {
        rr = ldns_rr_list_rr(rrlist, i);
        if (ldns_rr_get_type(rr) == LDNS_RR_TYPE_A && ldns_rr_rd_count(rr) == 1) {
            if (!printing) {
                printing = true;
                output = dnsfile_flux();
                __print_ts(output, ts);
                fprintf(output, "\t");
                ldns_rdf_print(output, ldns_rr_owner(q));
                fprintf(output, "\t");
            }
            ldns_rdf_print(output, ldns_rr_rdf(rr, 0));
            fprintf(output, ",%d;", ldns_rr_ttl(rr));
        }
    }
    if (printing) {
        fprintf(output, "\n");
    }
    
}

void dnspkt_proc (const char *bytes, uint16_t len, struct timeval ts, host_t *src, host_t *dst) {
    
    ldns_pkt *pkt;
    if (ldns_wire2pkt(&pkt, bytes, len) != LDNS_STATUS_OK) {
        return;
    }
    
    if (ldns_pkt_get_opcode(pkt) == LDNS_PACKET_QUERY &&
            ldns_pkt_qr(pkt) == 1 &&
            ldns_pkt_qdcount(pkt) == 1) {
            dnspkt_tun(pkt, ts, dst);
            dnspkt_dga(pkt, ts, dst);
            dnspkt_flux(pkt, ts);
/*        
        if (dnsenv_isserv(src)) {
            dnspkt_tun(pkt, ts, dst);
            dnspkt_dga(pkt, ts, dst);
        } else if (dnsenv_isrecur(dst)) {
            dnspkt_flux(pkt, ts);
        }
*/
    }
    
    ldns_pkt_free(pkt);
    
}

#endif //__DNSPKT_H_
