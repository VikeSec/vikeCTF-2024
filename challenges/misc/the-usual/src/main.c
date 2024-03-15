#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "main.h"

const char *MENU =
    "\nPlease make a selection:\n"
    "1: A life-altering flag-themed quote, $10\n"
    "2: A hand-typed, bespoke, artist's rendition of the flag, $45\n"
    "3: An organic, custom-engraved flag stand, $130\n"
    "4: The flag, $20,000\n"
    "5: Exit\n\n";

const int QUOTE_PRICE = 10;
const int ART_PRICE = 45;
const int STAND_PRICE = 130;
const int FLAG_PRICE = 20000;

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);
  printf("Welcome to the flag shop!\n");
  main_loop();
}

void main_loop() {
  int balance = 100;

  while (1) {
    printf("%s", MENU);
    printf("Your balance is $%d\n", balance);

    unsigned int selection = 0;
    char *request = "What would you like to buy? (1-5) ";
    if (read_uint(&selection, request) == -1 || selection < 1 ||
        selection > 5) {
      printf("I'm afraid we don't sell that\n");
      continue;
    }

    if (selection == 5) {
      printf("Goodbye!\n");
      return;
    }

    unsigned int count = 0;
    request = "How many would you like? ";
    if (read_uint(&count, request) == -1) {
      printf("I can't sell that many\n");
      continue;
    }

    if (!can_afford(balance, count, selection)) {
      printf("You can't afford that\n");
      continue;
    }

    int i = 0;
    do {
      if (selection == 1) {
        balance -= QUOTE_PRICE;
        print_quote();
      } else if (selection == 2) {
        balance -= ART_PRICE;
        print_art();
      } else if (selection == 3) {
        balance -= STAND_PRICE;
        print_stand();
      } else if (selection == 4) {
        printf("Sorry, the flag is under maintenance\n");
      } else {
        printf("Goodbye!\n");
        return;
      }
      i++;
    } while (i < count);
  }
}

int read_uint(unsigned int *result, char *prompt) {
  char input_str[300];

  printf("%s", prompt);
  if (fgets(input_str, sizeof(input_str), stdin) == NULL) {
    return -1;
  }

  if (strncmp(input_str, "0\n", 3) == 0 || strncmp(input_str, "\n", 2) == 0) {
    return -1;
  }

  *result = strtoul(input_str, NULL, 10);
  return 0;
}

int can_afford(int balance, unsigned int count, unsigned int selection) {
  int price;

  if (selection == 1) {
    price = QUOTE_PRICE;
  } else if (selection == 2) {
    price = ART_PRICE;
  } else if (selection == 3) {
    price = STAND_PRICE;
  } else if (selection == 4) {
    price = FLAG_PRICE;
  } else {
    price = 0;
  }

  if (balance > (price * count)) {
    return 1;
  }

  return 0;
}

void print_quote() { printf("I see the flag! It's so... flappy!\n"); }

void print_art() {
  printf("  (_)\n"
         "   |       _,--,_\n"
         "   |-:'--~'      |\n"
         "   | :           |\n"
         "   | :     _,--,_|\n"
         "   |-:'--~'\n"
         "   |\n"
         "   |\n"
         "   |\n"
         "   |\n"
         "   |\n"
         "   |\n"
         "-------\n");
}

void print_stand() {
  char stand[30];
  printf("What would you like your flag stand to say? ");
  fgets(stand, 300, stdin);

  printf("Great! Your organic, custom-engraved flag stand will be delivered "
         "within three to six business weeks\n");
}

void print_flag() {
  FILE *fp = fopen("flag.txt", "r");

  if (fp == NULL) {
    printf("Couldn't find the flag!\n");
    return;
  }

  char ch;
  while ((ch = fgetc(fp)) != EOF) {
    printf("%c", ch);
  }

  fclose(fp);
}
