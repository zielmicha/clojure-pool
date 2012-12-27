#include <unistd.h>
#include "DupHelper.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

JNIEXPORT void JNICALL Java_DupHelper_reopen
(JNIEnv * env, jclass cls, jstring fn, jint fd, jboolean write) {
  const char* cfn;
  cfn = (*env)->GetStringUTFChars(env, fn, NULL);
  if (cfn == NULL) {
    return;
  }

  int newfd = open(cfn, write? (O_APPEND | O_WRONLY) : (O_RDONLY));
  dup2(newfd, fd);
  // close(newfd); // ?

  (*env)->ReleaseStringUTFChars(env, fn, cfn);
}
