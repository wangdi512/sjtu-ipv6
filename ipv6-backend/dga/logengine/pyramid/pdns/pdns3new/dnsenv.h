#ifndef __DNSENV_H_
#define __DNSENV_H_

#include <stdint.h>
#include <endian.h>

inline bool dnsenv_isserv (host_t *ip) {
    
    if (ip->ipver == 4) {
        if (ip->ip4 == 0xCA780264) return true; // 202.120.2.100
        if (ip->ip4 == 0xCA780265) return true; // 202.120.2.101
        if (ip->ip4 == 0xCA701A28) return true; // 202.112.26.40
    }
    return false;
}

inline bool dnsenv_isrecur (host_t *ip) {
    
    if (ip->ipver == 4) {
        if (ip->ip4 == 0xCA780264) return true; // 202.120.2.100
        if (ip->ip4 == 0xCA7802AB) return true; // 202.120.2.171
        if (ip->ip4 == 0xCA7802AA) return true; // 202.120.2.170
        if (ip->ip4 == 0xCA780259) return true; // 202.120.2.89
        if (ip->ip4 == 0xCA7802A9) return true; // 202.120.2.169
        if (ip->ip4 == 0xCA7802A8) return true; // 202.120.2.168
        if (ip->ip4 == 0xCA701A2A) return true; // 202.112.26.42
    }
    
    return false;
}

#endif //__DNSENV_H_
