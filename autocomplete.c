#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "autocomplete.h"

int compare_term(const void *a, const void *b)
{
  return strcmp(((term *)a)->term, ((term *)b)->term);
}

void read_in_terms(term **terms, int *pnterms, char *filename)
{
    FILE *fp = fopen(filename, "r");
    
    char line[200];
    int count = -1;
    while (fgets(line, sizeof(line), fp) != NULL){
        count++;
    }

    fseek(fp, 0, SEEK_SET);

    *terms = (term *)malloc(count * sizeof(term));

    for (int i = 0; i < count; i++) {
        if (fgets(line, sizeof(line), fp) != NULL){
          int j = 0;
          char *temp_weight = malloc(200 * sizeof(char));
          int r = 0;
          while(line[j] != '\t'){
            temp_weight[r] = line[j];
            j++;
            r++;
          }
          j++;
          temp_weight[r] = '\0';

          (*terms)[i].weight = atoi(temp_weight);
          free(temp_weight);
        
          char *temp = malloc(200 * sizeof(char));
          int k = 0;
          while(line[j] != '\n'){
            temp[k] = line[j];
            k++;
            j++;
          }
          temp[k] = '\0';

          strcpy((*terms)[i].term, temp);
          free(temp);
        }
    }

    fclose(fp);
    qsort(*terms, count, sizeof(term), compare_term);
    *pnterms = count;
}

int lowest_match(term *terms, int nterms, char *substr)
{
    int left = 0;
    int right = nterms - 1;
    int match = -1;

    while(left <= right){
      int mid = left + ((right - left) / 2);
      if (strncmp(terms[mid].term, substr, strlen(substr)) == 0){
          match = mid;
          right = mid - 1;
      } 
      else if (strncmp(terms[mid].term, substr, strlen(substr)) < 0){
          left = mid + 1;
      } 
      else{
          right = mid - 1;
      }
    }
    return match;
}

int highest_match(term *terms, int nterms, char *substr)
{
    int left = 0;
    int right = nterms - 1;
    int match = -1;

    while(right >= left){
      int mid = left + ((right-left) / 2);
      if (strncmp(terms[mid].term, substr, strlen(substr)) == 0){
          match = mid;
          left = mid + 1;
      } 
      else if (strncmp(terms[mid].term, substr, strlen(substr)) < 0){
          left = mid + 1;
      } 
      else{
           right = mid - 1;
      }
    }
    return match;
}

int compare_weight(const void *a, const void *b) {
    const term *term_a = (const term *)a;
    const term *term_b = (const term *)b;

    if (term_a->weight < term_b->weight)
        return 1;
    else if (term_a->weight > term_b->weight)
        return -1;
    else
        return 0;
}

void autocomplete(term **answer, int *n_answer, term *terms, int nterms, char *substr)
{
  int high = highest_match(terms,nterms,substr);
  int low = lowest_match(terms,nterms,substr);
  *n_answer = high - low;

  *answer = (term *)malloc((*n_answer)*sizeof(term));
  
  for (int i = 0; low < high; low++, i++){
    strcpy((*answer)[i].term, terms[low].term);
    (*answer)[i].weight = terms[low].weight;
  }

  qsort(*answer, *n_answer, sizeof(term), compare_weight);
}