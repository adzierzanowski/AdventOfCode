#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


char *bigint_add(char *a, char *b) {
  size_t alen = strlen(a);
  size_t blen = strlen(b);
  size_t maxlen = alen < blen ? blen : alen;
  size_t minlen = alen < blen ? alen : blen;
  char *maxnum = alen < blen ? b : a;
  char *minnum = alen < blen ? a : b;

  char *result = calloc(sizeof (char), alen+2);

  int offset = maxlen - minlen;

  int m = 0;

  for (int i = maxlen-1; i >= 0; i--) {
    uint8_t mindig = ((i-offset >= 0) ? minnum[i-offset] : '0') - '0';
    uint8_t maxdig = maxnum[i] - '0';
    uint8_t res = maxdig + mindig + m;
    char resdig = res%10 + '0';
    m = res / 10;
    result[i] = resdig;
  }

  if (m > 0) {
    memmove(result+1, result, strlen(result));
    result[0] = m + '0';
  }

  return result;
}

void next_day(char **fish) {
  char *tmp = fish[0];
  for (int i = 0; i < 9; i++) {
    fish[i] = fish[i+1];
  }
  fish[8] = tmp;

  char *fish6 = bigint_add(tmp, fish[6]);
  free(fish[6]);
  fish[6] = fish6;
}




int main(int argc, char *argv[]) {

  if (argc < 2) {
    fprintf(stderr, "Please provide a path to input data.\n");
    return 1;
  }

  clock_t start = clock();

  // LOAD AND PARSE
  int fishint[9] = {0};

  FILE *f = fopen(argv[1], "r");

  for (;;) {
    char tmp = 0;
    size_t cnt = fread(&tmp, 1, 1, f);

    if (tmp == '\n') {
      break;
    } else if (tmp != ',') {
      fishint[tmp-'0']++;
    }

    if (!cnt) break;
  }

  fclose(f);

  char *fish[9] = {NULL};

  for (int i = 0; i < 9; i++) {
    char *afish = NULL;
    size_t needed = snprintf(afish, 0, "%d", fishint[i]);
    afish = calloc(sizeof(char), needed+1);
    sprintf(afish, "%d", fishint[i]);
    fish[i] = afish;
  }




  // PART 1
  for (int i = 0; i < 80; i++) {
    next_day(fish);
  }

  char *sum = calloc(sizeof (char), 2);
  sum[0] = '0';

  for (int i = 0; i < 9; i++) {
    char *tmp = bigint_add(sum, fish[i]);
    free(sum);
    sum = tmp;
  }

  printf("%s\n", sum);
  free(sum);






  // PART 2
  for (int i = 80; i < 256; i++) {
    next_day(fish);
  }

  sum = calloc(sizeof (char), 2);
  sum[0] = '0';

  for (int i = 0; i < 9; i++) {
    char *tmp = bigint_add(sum, fish[i]);
    free(sum);
    sum = tmp;
  }

  printf("%s\n", sum);
  free(sum);

  for (int i = 0; i < 9; i++) {
    free(fish[i]);
  }

  clock_t end = clock();


  double took = (double) (end - start) / CLOCKS_PER_SEC;

  printf("took %lf s\n", took);

  return 0;
}
