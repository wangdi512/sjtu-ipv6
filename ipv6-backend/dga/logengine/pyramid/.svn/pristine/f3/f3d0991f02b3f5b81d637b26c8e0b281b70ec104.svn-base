#ifndef __DNSCACHE_H_
#define __DNSCACHE_H_

#include <unordered_map>
#include <iostream>
#include <string>
using namespace std;

#include <regex.h>

unordered_map <string, bool> cache_rr;
uint32_t cache_rr_drop = 0;
uint32_t cache_rr_hit = 0;
uint32_t cache_rr_miss = 0;
uint32_t cache_rr_time = 0;

regex_t regex_rootgtld;

void dnscache_init () {
    if (regcomp(&regex_rootgtld, "[[:blank:]][a-z].\\(root\\|gtld\\)-servers.net.", REG_ICASE | REG_NOSUB)) {
        fprintf(stderr, "Error: Could not compile regex\n");
        exit(1);
    }
}

bool dnscache_rr (char *data) {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 600;
    if (now.tv_sec != cache_rr_time) {
        cache_rr_time = now.tv_sec;
        cache_rr.clear();
        fprintf(stdout, "Cache statistics: Hit %u, Drop %u, Miss %u\n", cache_rr_hit, cache_rr_drop, cache_rr_miss);
        cache_rr_drop = 0;
        cache_rr_hit = 0;
        cache_rr_miss = 0;
    }
    if (regexec(&regex_rootgtld, data, 0, NULL, 0) == 0) {
        cache_rr_drop++;
        return true;
    }
    string cppdata = data;
    if (cache_rr.count(cppdata) > 0) {
        cache_rr_hit++;
        return true;
    } else {
        cache_rr_miss++;
        cache_rr.emplace(cppdata, 1);
        return false;
    }
}


#endif //__DNSCACHE_H_

