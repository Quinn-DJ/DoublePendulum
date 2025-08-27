#include "DoublePendulum.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    std::string configFile = "./config/config";
    std::string dataFile = "pendulum_data.txt";
    
    // 解析命令行参数
    if (argc >= 2) {
        configFile = argv[1];
    }
    if (argc >= 3) {
        dataFile = argv[2];
    }
    
    std::cout << "双摆模拟程序 - 使用Verlet算法" << std::endl;
    std::cout << "配置文件: " << configFile << std::endl;
    std::cout << "数据输出文件: " << dataFile << std::endl;
    std::cout << "=================================" << std::endl;
    
    try {
        // 加载配置
        Config config = DoublePendulum::loadConfig(configFile);
        
        std::cout << "配置参数:" << std::endl;
        std::cout << "  摆长: L1=" << config.L1 << "m, L2=" << config.L2 << "m" << std::endl;
        std::cout << "  质量: M1=" << config.M1 << "kg, M2=" << config.M2 << "kg" << std::endl;
        std::cout << "  重力: g=" << config.G << "m/s²" << std::endl;
        std::cout << "  初始角度: θ1=" << config.theta1 << "rad, θ2=" << config.theta2 << "rad" << std::endl;
        std::cout << "  初始角速度: ω1=" << config.omega1 << "rad/s, ω2=" << config.omega2 << "rad/s" << std::endl;
        std::cout << "  时间步长: dt=" << config.dt << "s" << std::endl;
        std::cout << "  模拟时间: " << config.totalTime << "s" << std::endl;
        std::cout << "=================================" << std::endl;
        
        // 创建双摆对象
        DoublePendulum pendulum(config);
        
        // 运行模拟并输出数据
        pendulum.simulateAndOutputData(dataFile);
        
        std::cout << "程序执行完成！" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
