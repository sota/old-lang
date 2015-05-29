#ifndef __SOTA_DENTER_HELPER__
#define __SOTA_DENTER_HELPER__ = 1

#include <vector>
#include <sstream>
#include <iostream>
#include <exception>
#include <stdexcept>

class DenterException: public std::runtime_error {
    static std::ostringstream oss;
    int spaces;
    int indents;
    int dentsize;
public:
    DenterException(int spaces, int indents, int dentsize)
        : std::runtime_error("Denter Exception")
        , spaces(spaces)
        , indents(indents)
        , dentsize(dentsize) {}

    virtual const char * what() const throw() {
        oss.str("");
        oss
            << std::runtime_error::what()
            << ": spaces=" << this->spaces
            << "indents=" << this->indents
            << "dentsize=" << this->dentsize << std::endl;
        return oss.str().c_str();
    }
};
std::ostringstream DenterException::oss;

class LexerHelper {
    int indents;
    int dentsize;
    std::vector<const char *> newlines;
public:
    LexerHelper(const char *pchar) : indents(0), dentsize(0) {
        if (pchar)
            this->newlines.push_back(pchar);
    }
    ~LexerHelper() {
        this->newlines.clear();
    }
    void add_newline(const char *pchar) {
        if (pchar > this->newlines.back())
            this->newlines.push_back(pchar);
        else
            printf("UNEXPECTED BEHAVIOR!!!\n");
    }
    const char * newline(const char *pchar) {
        for (unsigned i = this->newlines.size(); i-- > 0;) {
            if (pchar > this->newlines[i])
                return this->newlines[i];
        }
        return 0;
    }
    long line(const char *pchar) {
        for (unsigned i = this->newlines.size(); i-- > 0;) {
            if (pchar > this->newlines[i])
                return i + 1;
        }
        return 0;
    }
    long pos(const char *pchar) {
        const char *nl = this->newline(pchar);
        if (nl)
            return pchar - nl;
        return 0;
    }
    int is_dent(int spaces) {
        int result = 0;
        if (this->dentsize == 0)
            this->dentsize = spaces;
        if (spaces == this->indents + this->dentsize)
            result = 1;
        else if (spaces == this->indents - this->dentsize)
            result = -1;
        else if (spaces == indents)
            result = 0;
        else
            throw DenterException(spaces, this->indents, this->dentsize);
        this->indents = spaces;
        return result;
    }
    int dents() {
        if (this->dentsize)
            return this->indents / this->dentsize;
        return 0;
    }
};





#endif /*__SOTA_DENTER_HELPER__*/
