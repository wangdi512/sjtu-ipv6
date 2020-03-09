#ifndef __DNSFILE_H_
#define __DNSFILE_H_

#include <stdlib.h>
#include <string.h>
#include <stdint.h>

FILE *file_resp = NULL;
uint32_t time_resp = 0;

FILE *dnsfile_resp () {
    struct timeval now;
    gettimeofday(&now, NULL);
    now.tv_sec = now.tv_sec - now.tv_sec % 3600;
    if (file_resp == NULL || now.tv_sec != time_resp) {
        if (file_resp != NULL) {
            fclose(file_resp);
            file_resp = NULL;
        }
        time_resp = now.tv_sec;
        char filename[32];
        struct tm *now_tm = localtime(&(now.tv_sec));
        strftime(filename, sizeof filename, "resp_%Y%m%d_%H.log", now_tm);
        file_resp = fopen(filename, "a");
        if (file_resp == NULL) {
            fprintf(stderr, "Error: Unable to open file for appending: %s\n", filename);
            return stdout;
        }
    }
    return file_resp;
}

#endif //__DNSFILE_H_

