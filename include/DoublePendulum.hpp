#ifndef DOUBLE_PENDULUM_HPP
#define DOUBLE_PENDULUM_HPP

#include <vector>
#include <string>
#include <cmath>

struct Config {
    double L1, L2;       // 摆长
    double M1, M2;       // 质量
    double G;            // 重力加速度
    double theta1, theta2;   // 初始角度
    double omega1, omega2;   // 初始角速度
    double dt;           // 时间步长
    double totalTime;    // 总时间
};

struct Point {
    double x, y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}
};

class DoublePendulum {
private:
    Config config;
    double theta1, theta2;
    double omega1, omega2;
    double theta1_old, theta2_old;
    double omega1_old, omega2_old;
    
public:
    DoublePendulum(const Config& cfg);
    
    // 加载配置文件
    static Config loadConfig(const std::string& filename);
    
    // Verlet算法计算下一步
    void verletStep();
    
    // 计算加速度
    void calculateAcceleration(double& alpha1, double& alpha2);
    
    // 运行模拟并输出数据到文件
    void simulateAndOutputData(const std::string& dataFilename);
    
    // 获取球的位置
    Point getPendulum1Position();
    Point getPendulum2Position();
};

#endif
