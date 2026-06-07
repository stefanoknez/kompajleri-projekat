#ifndef SEMANT_H_
#define SEMANT_H_

//
// semant.h — declarations for the Cool semantic analyzer (PA3).
//
// The analysis itself is driven by program_class::semant() (implemented in
// semant.cc).  All the heavy machinery — the inheritance graph, the object
// (variable) environment and the method table — is kept file-local in
// semant.cc, so this header only needs to pull in the shared support code.
//

#include <assert.h>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <algorithm>
#include "cool-tree.h"
#include "stringtab.h"
#include "symtab.h"
#include "list.h"

#define TRUE 1
#define FALSE 0

#endif
