#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <stdint.h>

char *loaddata(const char *filename, int *nread) {
  FILE *f = fopen(filename, "r");
  char *out = NULL;

  int cread = 0;
  char c = 0;
  while (fread(&c, sizeof (char), 1, f) != 0) {
    if (c != '\n') {
      cread++;
      out = realloc(out, cread * sizeof (char));
      out[cread-1] = c;
    }
  }

  *nread = cread;
  fclose(f);
  return out;
}

void pt1(char *data, int nread) {
  int sum = 0;
  for (int i = 0; i < nread; i++) {
    int n = data[i];
    int m = data[(i+1) % nread];
    if (n == m) {
      sum += n - 48;
    }
  }

  printf("pt1: %d\n", sum);
}

void pt2(char *data, int nread) {
  int sum = 0;
  for (int i = 0; i < nread; i++) {
    int n = data[i];
    int m = data[(i + nread/2) % nread];
    if (n == m) {
      sum += n - 48;
    }
  }
  printf("pt2: %d\n", sum);
}

uint64_t us() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec * 1000000 + tv.tv_usec;
}

int main(int argc, char *argv[]) {
  clock_t start_c = clock();
  uint64_t start = us();

  int nread = 0;
  char *data = loaddata("day1.txt", &nread);

  printf("us = %llu\n", us());
  pt1(data, nread);
  pt2(data, nread);


  free(data);

  clock_t stop_c = clock();
  uint64_t stop = us();

  printf("took %llu us (via timeval)\n", stop-start);
  printf("took %0.0llf us (via clock_t)\n", ((double) stop_c-(double)start_c)/CLOCKS_PER_SEC * 1000000.0);

  return 0;
}
