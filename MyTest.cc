#ifdef STANDARD
/* STANDARD is defined, don't use any mysql functions */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#ifdef __WIN__
typedef unsigned __int64 ulonglong;     /* Microsofts 64 bit types */
typedef __int64 longlong;
#else
typedef unsigned long long ulonglong;
typedef long long longlong;
#endif /*__WIN__*/
#else
#include <my_global.h>
#include <my_sys.h>
#endif
#include <mysql.h>
#include <ctype.h>
static pthread_mutex_t LOCK_hostname;


extern "C" long long MyTest(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error) {
    return 0;
}

extern "C" long long MyTest_init(UDF_INIT *initid, UDF_ARGS *args,
                               char *message)
{
        // The most important thing to do here is setting up the memory
        // you need...
        // Lets say we need a lonlong type variable to keep a checksum
        // Although we do not need one in this case
//        longlong* i = new longlong; // create the variable
//        *i = 0;                     // set it to a value
//
//        // store it as a char pointer in the pointer variable
//        // Make sure that you don`t run in typecasting troubles later!!
//        initid->ptr = (char*)i;
//
//        // check the arguments format
//        if (args->arg_count != 1)
//        {
//            strcpy(message,"MyTest() requires one arguments");
//            return 1;
//        }
//
//        if (args->arg_type[0] != INT_RESULT)
//        {
//            strcpy(message,"MyTest() requires an integer");
//            return 1;
//        }
        return 0;
}

extern "C" void MyTest_deinit(UDF_INIT *initid)
{
        // Here you have to free the memory you allocated in the
        // initialization function
//        delete (longlong*)initid->ptr;
}

int main() {
	return 0;
}
