#ifndef __DNSFILE_H_
#define __DNSFILE_H_

#include <stdlib.h>
#include <string.h>
#include <stdint.h>

FILE *file_qry = NULL;
FILE *file_resp = NULL;
FILE *file_rr = NULL;
uint32_t time_qry = 0;
uint32_t time_resp = 0;
uint32_t time_rr = 0;

FILE *dnsfile_qry () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 600;
    if (file_qry == NULL || now.tv_sec != time_qry) {
        time_qry = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "qry_%Y%m%d_%H%M.log", now_tm);
        file_qry = fopen(filename, "a");
        if (file_qry == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_qry;
}

FILE *dnsfile_resp () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 600;
    if (file_resp == NULL || now.tv_sec != time_resp) {
        time_resp = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "resp_%Y%m%d_%H%M.log", now_tm);
        file_resp = fopen(filename, "a");
        if (file_resp == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_resp;
}

FILE *dnsfile_rr () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 600;
    if (file_rr == NULL || now.tv_sec != time_rr) {
        time_rr = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "rr_%Y%m%d_%H%M.log", now_tm);
        file_rr = fopen(filename, "a");
        if (file_rr == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_rr;
}


#endif //__DNSFILE_H_

