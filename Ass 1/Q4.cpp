#include <iostream> 
#include <string>
using namespace std;
string some_hash(const string& input) 
{ 
    string retval = "\x0f\xff\x00";
    for (size_t i = 0; i < input.length(); ++i) 
    {
        retval[0] ^= input[i]; retval[1] &= input[i]; retval[2] |= input[i]; } return retval;     
    }
}
