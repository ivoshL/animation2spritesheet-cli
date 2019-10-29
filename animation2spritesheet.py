from PIL import Image
import os
import sys

def print_usage():
    print ('Usage:')
    print ('python animation2spritesheet.py n file1 file2 file3 ... fileN outfile')
    print ('    n - number of images in each row')
    print ('    fileN - the path to the png file(s) or directory containing png file(s)')
    print ('    outfile - output file path')

def check_valid_args():
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)
    try:
        sys.argv[1] = int(sys.argv[1])
        if sys.argv[1] < 1:
            raise Exception()
    except:
        print_usage()
        print('n must be a number greater than 0')
        sys.exit(1)

    files = sys.argv[2:-1]
    png_files = []
    for f in files:
        if os.path.isdir(f):
            print(f)
            png_files.extend([os.path.join(f,ff) for ff in os.listdir(f) if ff.endswith('png')])
        elif os.path.isfile(f) and f.endswith('png'):
            png_files.append(f)

    # check if all image dimensions are the same
    pngs = [Image.open(f) for f in png_files]
    n_per_row = sys.argv[1]
    w, h = 0,0
    for i in range(len(pngs)-1):
        if (pngs[i].size != pngs[i+1].size):
            print ('all images must be have the same dimensions')
            sys.exit(1)
        w,h = pngs[i].size

    print ('converting files to spritesheet:')
    spritesheet = Image.new('RGBA', (min(n_per_row,len(pngs)) * w, round(len(pngs)/n_per_row) * h))

    x_offset = 0
    y_offset = 0
    for f,png in zip(png_files, pngs):
        print (f)
        spritesheet.paste(png, (x_offset, y_offset))
        x,y = png.size
        x_offset += x
        if x_offset >= spritesheet.size[0]:
            x_offset = 0
            y_offset += y

    #spritesheet.show()

    if os.path.exists(sys.argv[-1]):
        y = input(f'{sys.argv[-1]} exists, would you like to overwrite it? y/n')
        if y != 'y':
            sys.exit(1)
    print(f'saving {sys.argv[-1]}...')
    spritesheet.save(sys.argv[-1])

def main():
    check_valid_args()
    
    


if __name__ == '__main__':
    main()