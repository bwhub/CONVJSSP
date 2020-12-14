/* -*- mode: C++; c-basic-offset: 2; indent-tabs-mode: nil -*- */
/*
 *  Main authors:
 *     Christian Schulte <schulte@gecode.org>
 *
 *  Copyright:
 *     Christian Schulte, 2001
 *
 *  This file is part of Gecode, the generic constraint
 *  development environment:
 *     http://www.gecode.org
 *
 *  Permission is hereby granted, free of charge, to any person obtaining
 *  a copy of this software and associated documentation files (the
 *  "Software"), to deal in the Software without restriction, including
 *  without limitation the rights to use, copy, modify, merge, publish,
 *  distribute, sublicense, and/or sell copies of the Software, and to
 *  permit persons to whom the Software is furnished to do so, subject to
 *  the following conditions:
 *
 *  The above copyright notice and this permission notice shall be
 *  included in all copies or substantial portions of the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 *  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 *  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include <gecode/driver.hh>
#include <gecode/int.hh>

using namespace Gecode;

int rnd(int n) {
  long long int r = static_cast<long long int>(Support::hwrnd()) * n;
  return r / UINT_MAX;
}

int factorial(int n) {
  int f = 1;
  for (int i=2; i<=n; i++)
    f *= i;
  return f;
}

void fill2(char f, int n) {
  if (n < 10) std::cout << f;
  std::cout << n;
}

void fill4(char f, int n) {
  if (n < 10) std::cout << f;
  if (n < 100) std::cout << f;
  if (n < 1000) std::cout << f;
  std::cout << n;
}

void fill5(char f, int n) {
  if (n < 10) std::cout << f;
  if (n < 100) std::cout << f;
  if (n < 1000) std::cout << f;
  if (n < 10000) std::cout << f;
  std::cout << n;
}

void fill6(char f, int n) {
  if (n < 10) std::cout << f;
  if (n < 100) std::cout << f;
  if (n < 1000) std::cout << f;
  if (n < 10000) std::cout << f;
  if (n < 100000) std::cout << f;
  std::cout << n;
}

class Permutation : public Space {
public:
  IntVarArray x;
  Permutation(int n) : x(*this, n, 0, n-1) {
    distinct(*this, x);
    branch(*this, x, INT_VAR_NONE(), INT_VAL_MIN());
  }

  Permutation(Permutation& p) : Space(p) {
    x.update(*this, p.x);
  }
  
  virtual Space* copy(void) {
    return new Permutation(*this);
  }
};
    
int main(int argc, char* argv[]) {
  // int k = 1000000; // Number of instances
  int k = 100000; // Number of instances
  int m_min = 10, m_max = 10; // Machines
  int n_min = 10, n_max = 10; // Jobs
  int d = 99; // Maximal duration
  
  int* fms = new int[m_max+1];
  int** ps = new int*[m_max+1];

  Rnd rnd(0);

  for (int m=m_min; m<=m_max; m++) {
    int fm = factorial(m);
    int* p = new int[m * fm];
    fms[m] = fm;
    ps[m] = p;
    Permutation* g = new Permutation(m);
    DFS<Permutation> e(g);
    delete g;
    int q=0;
    while (Permutation* s = e.next()) {
      for (int j=0; j<m; j++)
        p[q++] = s->x[j].val();
      delete s;
    }
  }

  std::cout << "namespace {" << std::endl << std::endl;
  
  for (int r=0; r<k; r++) {
    int n = n_min + rnd(n_max - n_min+1);
    int m = m_min + rnd(m_max - m_min+1);
    std::cout << "  const int t";
    fill5('0',r);
    std::cout << "[] = {" << std::endl;
    std::cout << "    " << n << ", " << m << ", "
              << "// Number of jobs and machines"
              << std::endl;
    for (int j=0; j<n; j++) {
      int q = rnd(fms[m]);
      std::cout << "    ";
      for (int i=0; i<m; i++) {
        std::cout << ps[m][m*q+i] << ", ";
        fill2(' ',rnd(d)+1);
        if ((i != n-1) || (j != m-1))
          std::cout << ", ";
      }
      std::cout << std::endl;
    }
    std::cout << "  };" << std::endl;
  }

  std::cout << std::endl;

  // The following code will not be executed
  if (1) {
  std::cout << "  const int* js[] = {" << std::endl;
  int l=8;
  for (int r=0; r<k; r++) {
    if (l == 8) {
      std::cout << std::endl << "    ";
      l=0;
    }
    l++;
    std::cout << "&t";
    fill5('0',r);
    if(r!=k-1){
      std::cout << "[0], ";
    }
    else{
      std::cout << "[0] " << std::endl;
      std::cout << "  };" << std::endl;
    }
  }


  std::cout << std::endl;
  
  std::cout << "  const char* name[] = {" << std::endl;
  l=8;
  for (int r=0; r<k; r++) {
    if (l == 8) {
      std::cout << std::endl << "    ";
      l=0;
    }
    l++;
    std::cout << "\"t";
    fill5('0',r);
    std::cout << "\", ";
  }
  std::cout << "    nullptr" << std::endl;
  std::cout << "  };" << std::endl;
  std::cout << std::endl;



  } // END of ``if(0)''
  std::cout << "}" << std::endl;
  return 0;
}

// STATISTICS: example-any

