/*
 * Copyright (C) 2011-2016 Intel Corporation. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in
 *     the documentation and/or other materials provided with the
 *     distribution.
 *   * Neither the name of Intel Corporation nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */


#include <stdarg.h>
#include <stdio.h>      /* vsnprintf */

#include "Enclave.h"
#include "Enclave_t.h"  /* print_string */
#include <sgx_trts.h>
#include "sgx_tseal.h"

#include <set>
#include <string>
using namespace std;


set<string> db;


/*
 * printf:
 *   Invokes OCALL to display the enclave buffer to the terminal.
 */
void printf(const char *fmt, ...)
{
    char buf[BUFSIZ] = {'\0'};
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, BUFSIZ, fmt, ap);
    va_end(ap);
    ocall_print_string(buf);
}


static inline void free_allocated_memory(void *pointer)
{
    if(pointer != NULL)
    {
        free(pointer);
        pointer = NULL;
    }
}


void ecall_insert_record(const char *str)
{
  string rec(str);
  db.insert(rec);
}

void ecall_delete_record(const char *str)
{
  string rec(str);
  db.erase(rec);
}

int ecall_query_record(const char *str)
{
  string rec(str);
  if (db.find(rec) == db.end())
    return 0;
  return 1;
}

int ecall_get_export_size() {
  int size = 0;
  for (set<string>::iterator it = db.begin(); it != db.end(); ++it)
    size += it->size() + 3;
  return size + sizeof(sgx_sealed_data_t);
}

int ecall_export_sealed_data(char* data, int size)
{
  if (data == NULL) {
    printf("Incorrect input parameter(s).\n");
    return -1;
  }
  string sdata;
  for (set<string>::iterator it = db.begin(); it != db.end(); ++it) {
    sdata.append(*it);
    sdata.append(SPLIT);
  }

  uint32_t sealed_len = size;
  uint8_t *plain_text = NULL;
  uint32_t plain_text_length = 0;
  uint8_t *temp_sealed_buf = (uint8_t *)malloc(sealed_len);


  sgx_status_t ret = sgx_seal_data(plain_text_length, plain_text, sdata.size(), (uint8_t *)&sdata[0], sealed_len, (sgx_sealed_data_t *)temp_sealed_buf);
  if(ret != SGX_SUCCESS)
  {
      printf("Failed to seal data\n");
      free_allocated_memory(temp_sealed_buf);
      return -1;
  }
  // Backup the sealed data to outside buffer
  memcpy(data, temp_sealed_buf, sealed_len);
  return 0;
}


/**
 * size: the size of the data
 */
int ecall_import_sealed_data(const char *data, int size) {

  // Retrieve the secret from current backup sealed data
  uint32_t unsealed_data_length = size - sizeof(sgx_sealed_data_t);
  char unsealed_data[unsealed_data_length];
  uint8_t *plain_text = NULL;
  uint32_t plain_text_length = 0;
  uint8_t *temp_sealed_buf = (uint8_t *)malloc(size);
  if(temp_sealed_buf == NULL)
  {
      printf("Out of memory.\n");
      return -1;
  }

  memcpy(temp_sealed_buf, data, size);

  // Unseal current sealed buf
  sgx_status_t ret = sgx_unseal_data((sgx_sealed_data_t *)temp_sealed_buf, plain_text, &plain_text_length, (uint8_t *)&unsealed_data, &unsealed_data_length);
  free_allocated_memory(temp_sealed_buf);
  if(ret != SGX_SUCCESS) {
      printf("Failed to unseal the data.\n");
      return -1;
  }

  db.clear();
  int begin = 0, end = 0;
  while (begin != unsealed_data_length) {
      if (unsealed_data[end] == '#' && unsealed_data[end + 1] == '.' && unsealed_data[end + 2] == '#') {
        db.insert(string(unsealed_data + begin, unsealed_data + end));
        begin = end = end + 3;
      }
      else
        end++;
  }

  return 0;
}
