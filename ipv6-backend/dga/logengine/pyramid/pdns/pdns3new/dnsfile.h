#ifndef __DNSFILE_H_
#define __DNSFILE_H_

#include <stdlib.h>
#include <string.h>
#include <stdint.h>

FILE *file_tun = NULL;
FILE *file_dga = NULL;
FILE *file_flux = NULL;
uint32_t time_tun = 0;
uint32_t time_dga = 0;
uint32_t time_flux = 0;

inline FILE *dnsfile_tun () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 300;
    if (file_tun == NULL || now.tv_sec != time_tun) {
        if (file_tun != NULL) {
            fclose(file_tun);
            file_tun = NULL;
        }
        time_tun = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "tun_%Y%m%d_%H%M.log", now_tm);
        file_tun = fopen(filename, "a");
        if (file_tun == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_tun;
}

inline FILE *dnsfile_dga () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 300;
    if (file_dga == NULL || now.tv_sec != time_dga) {
        if (file_dga != NULL) {
            fclose(file_dga);
            file_dga = NULL;
        }
        time_dga = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "dga_%Y%m%d_%H%M.log", now_tm);
        file_dga = fopen(filename, "a");
        if (file_dga == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_dga;
}

inline FILE *dnsfile_flux () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 300;
    if (file_flux == NULL || now.tv_sec != time_flux) {
        if (file_flux != NULL) {
            fclose(file_flux);
            file_flux = NULL;
        }
        time_flux = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "flux_%Y%m%d_%H%M.log", now_tm);
        file_flux = fopen(filename, "a");
        if (file_flux == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_flux;
}


#endif //__DNSFILE_H_

