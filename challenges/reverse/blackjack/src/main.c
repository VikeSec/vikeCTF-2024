#include <ctype.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

#define A 688885507887235759
#define C 128076673052050663

static uint32_t seed;

uint32_t rand(void) {
  seed = seed * A + C;
  return (uint32_t)(seed >> 16) & 0x7FFF;
}

static uint8_t cards_left = 0;
static uint16_t cards_bits = 0;

uint8_t draw(void) {
  if (cards_left == 0) {
    cards_bits = rand();
    cards_left = 2;
  }
  uint8_t card = (cards_bits & 0xFF) % 52;
  cards_bits >>= 8;
  cards_left -= 1;
  return card;
}

#define BUFLEN 256

uint8_t card_value(uint8_t card) {
  card = (card % 13) + 1;
  if (card > 10) {
    return 10;
  }
  return card;
}

void print_card(uint8_t card) {
  char suit = "shcd"[card / 13];
  card = (card % 13) + 1;
  if (card == 11) {
    printf("J");
  } else if (card == 12) {
    printf("Q");
  } else if (card == 13) {
    printf("K");
  } else {
    printf("%d", card);
  }
  printf("%c", suit);
}

uint64_t sum_hand(uint8_t *hand, uint8_t hand_len) {
  uint64_t sum = 0;
  for (int i = 0; i < hand_len; i++) {
    sum += card_value(hand[i]);
  }
  return sum;
}

void print_hand(uint8_t *hand, uint8_t hand_len) {
  for (int i = 0; i < hand_len; i++) {
    // printf("%" PRIu8 " ", hand[i]);
    print_card(hand[i]);
    printf(" ");
  }
  printf("(%" PRId64 ")\n", sum_hand(hand, hand_len));
}

uint64_t play_round(uint64_t balance) {
  printf("\nbalance: %" PRIu64 "\n", balance);
  printf("place your bet: ");
  fflush(stdout);

  uint64_t bet;
  scanf("%" SCNu64, &bet);

  if (bet > balance) {
    printf("you can't afford that, silly!\n");
    return balance;
  }

  uint8_t player_hand[256];
  player_hand[0] = draw();
  player_hand[1] = draw();
  uint8_t player_hand_len = 2;

  uint8_t house_hand[256];
  house_hand[0] = draw();
  house_hand[1] = draw();
  uint8_t house_hand_len = 2;

  printf("you: ");
  print_hand(player_hand, player_hand_len);
  printf("house: X ");
  print_card(house_hand[1]);
  printf("\n");

#define DUMP_HANDS                                                             \
  printf("your hand: ");                                                       \
  print_hand(player_hand, player_hand_len);                                    \
  printf("house hand: ");                                                      \
  print_hand(house_hand, house_hand_len)

#define WIN                                                                    \
  printf("win\n");                                                             \
  DUMP_HANDS;                                                                  \
  return balance + bet

#define LOSE                                                                   \
  printf("lose\n");                                                            \
  DUMP_HANDS;                                                                  \
  return balance - bet

#define PUSH                                                                   \
  printf("push\n");                                                            \
  DUMP_HANDS;                                                                  \
  return balance

  while (1) {
    printf("[h]it or [s]tand?\n");
    // you busted
    if (sum_hand(player_hand, player_hand_len) > 21) {
      LOSE;
    }

    char action;
    scanf(" %c", &action);
    action = toupper(action);

    if (action == 'S') {
      break;
    } else if (action == 'H') {
      player_hand[player_hand_len++] = draw();
      print_hand(player_hand, player_hand_len);
    }
  }

  while (1) {
    uint64_t sum = sum_hand(house_hand, house_hand_len);
    // house busted
    if (sum > 21) {
      WIN;
    } else if (sum >= 17) {
      break;
    } else {
      house_hand[house_hand_len++] = draw();
      print_hand(house_hand, house_hand_len);
    }
  }

  uint64_t player_sum = sum_hand(player_hand, player_hand_len);
  uint64_t house_sum = sum_hand(house_hand, house_hand_len);

  if (player_sum == house_sum) {
    PUSH;
  } else if (player_sum > house_sum) {
    WIN;
  } else {
    LOSE;
  }
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  seed = time(NULL);
  uint64_t balance = 100;

  printf("welcome to blackjack!\n");
  printf("to play, place a bet, and then hit [h] or stand [s]!\n");
  printf("if you win big, we might have a special surprise for you...\n");

  for (int i = 0; i < 50; i++) {
    if (balance == 0) {
      printf("you have no money, time to go home!\n");
      return 0;
    }
    balance = play_round(balance);
  }
  if (balance >= 100000000) {
    printf("you won! congrats!\n");
    FILE *flag = fopen("flag.txt", "r");
    char buf[1000];
    fgets(buf, sizeof(buf), flag);
    printf("i think you dropped this: %s\n", buf);
  } else {
    printf("it's closing time, thanks for playing!\n");
  }
  fflush(stdout);
}
