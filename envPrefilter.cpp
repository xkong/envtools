#include <iostream>
#include <getopt.h>
#include <cstdio>
#include <cstdlib>

#include "Cubemap"

static int usage(const std::string& name)
{
    std::cerr << "Usage: " << name << " [-s size] [-e stopSize] [-n nbsamples] in.tif out.tif" << std::endl;
    return 1;
}

int main(int argc, char *argv[])
{

    int size = 0;
    int c;
    int endSize = 1;
    int samples = 1024;

    while ((c = getopt(argc, argv, "s:e:n:")) != -1)
        switch (c)
        {
        case 's': size = atoi(optarg);       break;
        case 'e': endSize = atoi(optarg);  break;
        case 'n': samples = atoi(optarg);  break;

        default: return usage(argv[0]);
        }

    std::string input, output;
    if ( optind < argc-1 ) {

        // generate specular ibl
        input = std::string( argv[optind] );
        output = std::string( argv[optind+1] );

        Cubemap image;
        image.loadCubemap(input);
        image.computePrefilteredEnvironment( output, size, endSize, samples );

    } else {
        return usage( argv[0] );
    }


    return 0;
}