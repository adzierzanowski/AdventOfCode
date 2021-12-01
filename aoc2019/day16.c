#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>


const int pattern[4] = {0, 1, 0, -1};

int *evaluate(int *signal, size_t signal_sz) {
  int *out = calloc(signal_sz, sizeof(int));

  for (int i = 0; i < signal_sz; i++) {
    int val = 0;
    int reps = 1;
    int patptr = i == 0 ? 1 : 0;

    for (int j = 0; j < signal_sz; j++) {
      val += signal[j] * pattern[patptr % 4];
      reps++;
      if (reps >= (i+1)) {
        patptr++;
        reps = 0;
      }
    }

    out[i] = abs(val) % 10;
  }

  return out;
}

void print_signal(int *signal, size_t signal_sz) {
  for (int i = 0; i < signal_sz; i++) {
    printf("%d ", signal[i]);
  }
  printf("\n");
}

void print_first8(int *signal) {
  for (int i = 0; i < 8; i++) {
    printf("%d", signal[i]);
  }
  printf("\n");
}

int main(int argc, char *argv[])
{
  /*
  int signal[] = {
    5, 9, 7, 6, 2, 7, 7, 0, 7, 8, 1, 8, 1, 7, 7, 1, 9, 1, 9, 0, 4, 5, 9, 9, 2,
    0, 6, 3, 8, 9, 1, 6, 2, 9, 7, 9, 3, 2, 0, 9, 9, 9, 1, 9, 3, 3, 6, 4, 7, 3,
    8, 8, 0, 2, 0, 9, 1, 0, 0, 8, 3, 7, 3, 0, 9, 9, 5, 5, 1, 3, 3, 9, 4, 4, 7,
    7, 6, 1, 9, 6, 2, 9, 0, 1, 3, 1, 0, 6, 2, 9, 9, 1, 5, 8, 8, 5, 3, 3, 6, 0,
    4, 0, 1, 2, 7, 8, 9, 2, 7, 9, 7, 2, 2, 6, 9, 7, 4, 2, 7, 2, 1, 3, 1, 5, 8,
    6, 5, 1, 9, 6, 3, 8, 4, 2, 9, 4, 1, 0, 0, 0, 2, 2, 7, 6, 7, 5, 3, 6, 3, 2,
    6, 0, 5, 1, 3, 2, 8, 3, 3, 4, 9, 5, 6, 2, 6, 7, 4, 0, 0, 4, 0, 1, 5, 5, 9,
    3, 7, 3, 7, 5, 1, 8, 7, 5, 4, 4, 1, 3, 2, 3, 6, 2, 4, 1, 8, 7, 6, 9, 5, 9,
    8, 4, 0, 0, 7, 6, 3, 7, 2, 3, 9, 5, 8, 2, 1, 6, 2, 7, 4, 5, 1, 1, 7, 8, 9,
    2, 4, 6, 1, 9, 6, 0, 4, 7, 7, 8, 4, 8, 6, 9, 0, 3, 0, 4, 0, 6, 2, 1, 9, 1,
    6, 9, 0, 4, 5, 7, 5, 0, 5, 3, 1, 4, 1, 8, 2, 4, 9, 3, 9, 5, 2, 5, 9, 0, 4,
    6, 7, 6, 9, 1, 1, 2, 8, 5, 4, 4, 6, 8, 8, 9, 6, 8, 2, 0, 8, 9, 5, 6, 3, 0,
    7, 5, 5, 6, 2, 6, 4, 4, 8, 1, 3, 7, 4, 7, 2, 3, 9, 2, 8, 5, 3, 4, 4, 5, 2,
    2, 5, 0, 7, 6, 6, 6, 5, 9, 5, 5, 6, 1, 5, 7, 0, 2, 2, 9, 5, 7, 5, 0, 0, 9,
    1, 2, 1, 6, 6, 3, 3, 0, 3, 5, 1, 0, 7, 6, 3, 0, 1, 8, 8, 5, 5, 0, 3, 8, 1,
    5, 3, 9, 7, 4, 0, 9, 1, 4, 7, 1, 6, 2, 6, 3, 8, 0, 6, 3, 8, 0, 9, 8, 7, 4,
    0, 8, 1, 8, 1, 0, 2, 0, 8, 5, 5, 4, 2, 9, 2, 4, 9, 3, 7, 5, 2, 2, 5, 9, 5,
    3, 0, 3, 4, 6, 2, 7, 2, 5, 1, 4, 5, 6, 2, 0, 6, 7, 3, 3, 6, 6, 4, 7, 6, 9,
    8, 7, 4, 7, 3, 5, 1, 9, 9, 0, 5, 5, 6, 5, 3, 4, 6, 5, 0, 2, 4, 3, 1, 1, 2,
    3, 8, 2, 5, 7, 9, 8, 1, 7, 4, 3, 2, 6, 8, 9, 9, 5, 3, 8, 3, 4, 9, 7, 4, 7,
    4, 0, 4, 7, 8, 1, 6, 2, 3, 1, 9, 5, 2, 5, 3, 7, 0, 9, 2, 1, 2, 2, 0, 9, 8,
    8, 2, 5, 3, 0, 1, 3, 1, 8, 6, 4, 8, 2, 0, 6, 4, 5, 2, 7, 4, 9, 9, 4, 1, 2,
    7, 3, 8, 8, 2, 0, 1, 9, 9, 0, 7, 5, 4, 2, 9, 6, 0, 5, 1, 2, 6, 4, 0, 2, 1,
    2, 6, 4, 4, 9, 6, 6, 1, 8, 5, 3, 1, 8, 9, 0, 7, 5, 2, 4, 4, 6, 1, 4, 6, 4,
    6, 2, 0, 8, 8, 5, 7, 4, 4, 2, 6, 4, 7, 3, 9, 9, 8, 6, 0, 1, 1, 4, 5, 6, 6,
    5, 5, 4, 2, 1, 3, 4, 9, 6, 4, 0, 4, 1, 2, 5, 4, 9, 1, 9, 4, 3, 5, 6, 3, 5
  };
  */
  int signal[] = {0,3,0,3,6,7,3,2,5,7,7,2,1,2,9,4,4,0,6,3,4,9,1,5,6,5,4,7,4,6,6,4};
  size_t signal_sz = sizeof signal / sizeof signal[0];

  // PART 1
  int *tmp = malloc(signal_sz * sizeof(int));
  memcpy(tmp, signal, signal_sz * sizeof(int));

  for (int i = 0; i < 100; i++) {
    int *new_signal = evaluate(tmp, signal_sz);
    memcpy(tmp, new_signal, signal_sz * sizeof(int));
    free(new_signal);
  }

  print_first8(tmp);

  // PART 2
  tmp = realloc(tmp, sizeof(int) * signal_sz * 10000);
  //memcpy(tmp, signal, signal_sz * sizeof(int));
  for (int i = 0; i < 10000; i++) {
    memcpy(tmp+(i*signal_sz), signal, signal_sz * sizeof(int));
  }

  int *qqqq = evaluate(tmp, signal_sz * 10000);

  print_first8(qqqq);


  free(tmp);
  free(qqqq);

  return 0;
}
