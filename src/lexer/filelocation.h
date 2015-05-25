#ifndef __SOTA_FILE_LOCATION__
#define __SOTA_FILE_LOCATION__ = 1

#include <vector>
class FileLocation {
    std::vector<const char *> newlines;
public:
    FileLocation(const char *p) {
        if (p)
            this->newlines.push_back(p);
    }
    ~FileLocation() {
        this->newlines.clear();
    }
    void add_newline(const char *p) {
        if (p > this->newlines.back())
            this->newlines.push_back(p);
        else
            printf("UNEXPECTED BEHAVIOR!!!\n");
    }
    const char * get_newline(const char *p) {
        for (unsigned i = this->newlines.size(); i-- > 0;) {
            if (p > this->newlines[i])
                return this->newlines[i];
        }
        return 0;
    }
    long line(const char *p) {
        for (unsigned i = this->newlines.size(); i-- > 0;) {
            if (p > this->newlines[i])
                return i + 1;
        }
        return 0;
    }
    long pos(const char *p) {
        const char *nl = this->get_newline(p);
        if (nl)
            return p - nl;
        return 0;
    }
};

#endif /*__SOTA_FILE_LOCATION__*/
