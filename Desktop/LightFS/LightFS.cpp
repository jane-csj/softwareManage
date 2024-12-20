#include <iostream>
#include<fstream>
#include<vector>
#include<cstring>
#include<algorithm>

struct SuperBlock {
    char version[32];
    uint64_t totalSize;
    uint64_t usedSize;
};

struct Inode {
    std::string name;
    uint64_t size;
    uint32_t blockIndexs[200];
    Inode() :size(0), name(""), blockIndexs{ 0 } {
        
    }
    Inode(const std::string& name, uint64_t size, uint32_t* blockIndexes)
        : name(name), size(size) {
        for (int i = 0; i < 200; ++i) {
            blockIndexes[i] = 0;
        }
    }
};

struct DirEntry {
    std::string name;
    uint32_t inodeIndex;
    DirEntry(const std::string& name, uint32_t inodeIndex) :name(name), inodeIndex(inodeIndex) {

    }
};

const size_t LIGHT_SIZE = 256 * 1024 * 1024;//256mb
const size_t SUBERBLOCK_SIZE = 1024;
const size_t BLOCK_SIZE = 1024;//1mb块大小
const size_t BITMAP_SIZE = 25;//200bit
const size_t INODE_TABLE_SIZE = 1024 * 128;//1024inodes，每个128byte
const size_t ROOT_DIR_OFFSET = SUBERBLOCK_SIZE + BITMAP_SIZE + INODE_TABLE_SIZE;
const size_t DATA_AREA_OFFSET = 56 * 1024 * 1024;

SuperBlock superblock;
std::vector<char> bitmap(BITMAP_SIZE);//位图
std::vector<Inode> inodes;
std::vector<DirEntry> rootDir;
std::fstream fsFile;
//std::ifstream fsRead;

bool createFile(const std::string& fileName) {
    //检查是否有同名文件
    for (auto& entry : rootDir) {
        if (entry.name == fileName) {
            std::cerr << "File already exists." << std::endl;
            return false;
        }
    }

    
    uint32_t blockIndexes[200] = { -1 };
    Inode newInode(fileName, 0, blockIndexes);
    const char* content = "hello"+'\0';
    size_t contentLength = strlen(content);

    for (size_t i = 0; i < BITMAP_SIZE * 8; ++i) {
        /*
        * 检查bitmap的第i位是否为0
        * i/8表示的i位在这个bitmap的位置，第几个bitmap
        * (1<<(i%8))表示在这个bitmap中对应位为1的二进制
        * &按位与操作，当对应的位都为1时结果为1，即只看第i位是否可用（为0）
        */
        if ((bitmap[i / 8] & (1 << (i % 8))) == 0) {
            //按位或对应位使用
            bitmap[i / 8] |= (1 << (i % 8));

            //找到的第一个可用数据块索引i
            newInode.blockIndexs[0] = static_cast<uint32_t>(i);
            newInode.size = contentLength;

            inodes.push_back(newInode);
            uint32_t inodeIndex = static_cast<uint32_t>(inodes.size() - 1);
            DirEntry newEntry(fileName, inodeIndex);
            rootDir.push_back(newEntry);

            //将内容写入数据块
            fsFile.seekp(DATA_AREA_OFFSET + i * 1024 * 1024, std::ios_base::beg);
            fsFile.write(content, contentLength);

            //更新索引节点表
            fsFile.seekp(SUBERBLOCK_SIZE + BITMAP_SIZE + inodeIndex + sizeof(Inode), std::ios_base::beg);
            fsFile.write(reinterpret_cast<const char*>(&newInode), sizeof(Inode));

            //更新超级块中的已用空间
            SuperBlock superBlock;
            fsFile.seekg(0, std::ios_base::beg);
            fsFile.read(reinterpret_cast<char*>(&superBlock), sizeof(SuperBlock));
            superBlock.usedSize += contentLength;
            

            fsFile.seekp(0, std::ios_base::beg);
            fsFile.write(reinterpret_cast<const char*>(&superBlock), sizeof(SuperBlock));

            return true;
        }
    }

    // 如果没有找到可用的数据块
    std::cerr << "No available data blocks to allocate." << std::endl;
    return false;
}

void init() {
    fsFile = std::fstream("light.fs", std::ios::binary | std::ios::in | std::ios::out);
    if (!fsFile.is_open()) {
        std::cerr << "Failed to open light.fs" << std::endl;
        return;
    }

    //从light.fs中加载内容到std::vector<char> bitmap(BITMAP_SIZE);，std::vector<Inode> inodes;，std::vector<DirEntry> rootDir;
    
    //加载超级块
    fsFile.read(reinterpret_cast<char*>(&superblock),sizeof(superblock));
    
    //加载位图
    fsFile.read(bitmap.data(), BITMAP_SIZE);

    //加载inode表
    inodes.resize(1024 );
    fsFile.read(reinterpret_cast<char*>(inodes.data()), INODE_TABLE_SIZE);

    //设置目录
    uint32_t index = 0;
    for (auto& inode : inodes) {
        std::cout << inode.name.size() << std::endl;
        
        rootDir.push_back(DirEntry(inode.name, index++));
    }


    /*
    新创建的light.fs，最开始的初始化
    */

    //
    //SuperBlock superBlock = { "Light v1.0",LIGHT_SIZE,0 };
    //fsFile.write(reinterpret_cast<const char*>(&superBlock), sizeof(SuperBlock));

    //memset(bitmap.data(), 0, BITMAP_SIZE);
    //fsFile.write(bitmap.data(), BITMAP_SIZE);

    ////设置文件写入位置，已经在超级块和位图之后的位置
    //fsFile.seekp(INODE_TABLE_SIZE, std::ios::cur);

    ////根目录
    //fsFile.seekp(ROOT_DIR_OFFSET,std::ios::beg);

    ////填充剩余数据区为空
    //fsFile.seekp(DATA_AREA_OFFSET-fsFile.tellp(),std::ios::cur);
    //fsFile.seekp(LIGHT_SIZE - fsFile.tellp(), std::ios::cur);

    //fsFile.close();
}

void export_file(const std::string& filename) {
    // 查找文件名对应的索引节点
    uint32_t inodeIndex = -1;
    for (auto& entry : rootDir) {
        if (entry.name == filename) {
            inodeIndex = entry.inodeIndex;
            break;
        }
    }

    if (inodeIndex == static_cast<uint32_t>(-1)) {
        std::cerr << "File not found: " << filename << std::endl;
        return;
    }

    // 读取索引节点
    Inode inode = inodes[inodeIndex];

    // 创建输出文件
    std::ofstream outFile(filename, std::ios::binary | std::ios::trunc);
    if (!outFile.is_open()) {
        std::cerr << "Failed to create output file: " << filename << std::endl;
        return;
    }

    // 读取并写入文件内容
    size_t remainingSize = inode.size;
    for (size_t i = 0; i < 200 && remainingSize > 0; ++i) {
        if (inode.blockIndexs[i] != -1) {
            size_t blockOffset = DATA_AREA_OFFSET + inode.blockIndexs[i] * 1024;
            char buffer[1024];
            fsFile.seekg(blockOffset, std::ios_base::beg);
            fsFile.read(buffer, sizeof(buffer));

            // 只写入实际使用的部分
            size_t bytesToWrite = (remainingSize >= 1024) ? 1024 : remainingSize;
            outFile.write(buffer, bytesToWrite);
            remainingSize -= bytesToWrite;
        }
    }

    // 关闭文件
    outFile.close();
    std::cout << "File exported successfully: " << filename << std::endl;
}

int main()
{
    init();
    //createFile("example.txt");
    //fsRead.open("light.fs", std::ios::binary);
    //fsRead.close();
    //std::fstream fs("light.fs", std::ios::in | std::ios::out | std::ios::binary);
    //createFile("example.txt");


    /*if (createFile("example.txt")) {
        std::cout << "File created successfully." << std::endl;
    }
    else {
        std::cerr << "Failed to create file." << std::endl;
    }*/
    //export_file("example.txt");
    std::cout << "Hello World!\n";
}

