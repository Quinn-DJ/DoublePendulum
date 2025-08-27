#include "DoublePendulum.hpp"
#include <iostream>
#include <fstream>
#include <sstream>

DoublePendulum::DoublePendulum(const Config& cfg) : config(cfg) {
    theta1 = config.theta1;
    theta2 = config.theta2;
    omega1 = config.omega1;
    omega2 = config.omega2;
    
    // 初始化old值用于Verlet算法
    theta1_old = theta1;
    theta2_old = theta2;
    omega1_old = omega1;
    omega2_old = omega2;
}

Config DoublePendulum::loadConfig(const std::string& filename) {
    Config cfg;
    std::ifstream file(filename);
    std::string line;
    
    if (!file.is_open()) {
        std::cerr << "无法打开配置文件: " << filename << std::endl;
        // 设置默认值
        cfg.L1 = cfg.L2 = 1.0;
        cfg.M1 = cfg.M2 = 1.0;
        cfg.G = 9.81;
        cfg.theta1 = 1.5;
        cfg.theta2 = 1.0;
        cfg.omega1 = cfg.omega2 = 0.0;
        cfg.dt = 0.01;
        cfg.totalTime = 20.0;
        return cfg;
    }
    
    while (std::getline(file, line)) {
        // 跳过注释和空行
        if (line.empty() || line[0] == '#') continue;
        
        size_t pos = line.find('=');
        if (pos == std::string::npos) continue;
        
        std::string key = line.substr(0, pos);
        std::string value = line.substr(pos + 1);
        
        // 移除行内注释
        size_t comment_pos = value.find('#');
        if (comment_pos != std::string::npos) {
            value = value.substr(0, comment_pos);
        }
        
        // 移除前后空白字符
        key.erase(0, key.find_first_not_of(" \t"));
        key.erase(key.find_last_not_of(" \t") + 1);
        value.erase(0, value.find_first_not_of(" \t"));
        value.erase(value.find_last_not_of(" \t") + 1);
        
        if (key == "L1") cfg.L1 = std::stod(value);
        else if (key == "L2") cfg.L2 = std::stod(value);
        else if (key == "M1") cfg.M1 = std::stod(value);
        else if (key == "M2") cfg.M2 = std::stod(value);
        else if (key == "G") cfg.G = std::stod(value);
        else if (key == "THETA1") cfg.theta1 = std::stod(value);
        else if (key == "THETA2") cfg.theta2 = std::stod(value);
        else if (key == "OMEGA1") cfg.omega1 = std::stod(value);
        else if (key == "OMEGA2") cfg.omega2 = std::stod(value);
        else if (key == "DT") cfg.dt = std::stod(value);
        else if (key == "TOTAL_TIME") cfg.totalTime = std::stod(value);
    }
    
    file.close();
    return cfg;
}

void DoublePendulum::calculateAcceleration(double& alpha1, double& alpha2) {
    double L1 = config.L1, L2 = config.L2;
    double M1 = config.M1, M2 = config.M2;
    double g = config.G;
    
    double delta_theta = theta2 - theta1;
    double cos_delta = cos(delta_theta);
    double sin_delta = sin(delta_theta);
    
    double denom1 = (M1 + M2) * L1 - M2 * L1 * cos_delta * cos_delta;
    double denom2 = (L2 / L1) * denom1;
    
    // 计算第一个摆的角加速度
    alpha1 = (-M2 * L1 * omega1 * omega1 * sin_delta * cos_delta
              + M2 * g * sin(theta2) * cos_delta
              + M2 * L2 * omega2 * omega2 * sin_delta
              - (M1 + M2) * g * sin(theta1)) / denom1;
    
    // 计算第二个摆的角加速度
    alpha2 = (-M2 * L2 * omega2 * omega2 * sin_delta * cos_delta
              + (M1 + M2) * g * sin(theta1) * cos_delta
              + (M1 + M2) * L1 * omega1 * omega1 * sin_delta
              - (M1 + M2) * g * sin(theta2)) / denom2;
}

void DoublePendulum::verletStep() {
    double alpha1, alpha2;
    calculateAcceleration(alpha1, alpha2);
    
    // Verlet算法更新位置
    double theta1_new = 2 * theta1 - theta1_old + alpha1 * config.dt * config.dt;
    double theta2_new = 2 * theta2 - theta2_old + alpha2 * config.dt * config.dt;
    
    // 更新角速度（使用中心差分）
    omega1 = (theta1_new - theta1_old) / (2 * config.dt);
    omega2 = (theta2_new - theta2_old) / (2 * config.dt);
    
    // 更新位置
    theta1_old = theta1;
    theta2_old = theta2;
    theta1 = theta1_new;
    theta2 = theta2_new;
}

Point DoublePendulum::getPendulum1Position() {
    return Point(config.L1 * sin(theta1), -config.L1 * cos(theta1));
}

Point DoublePendulum::getPendulum2Position() {
    Point p1 = getPendulum1Position();
    return Point(p1.x + config.L2 * sin(theta2), 
                 p1.y - config.L2 * cos(theta2));
}

void DoublePendulum::simulateAndOutputData(const std::string& dataFilename) {
    double t = 0.0;
    int steps = static_cast<int>(config.totalTime / config.dt);
    
    // 打开数据输出文件
    std::ofstream dataFile(dataFilename);
    if (!dataFile.is_open()) {
        std::cerr << "无法创建数据文件: " << dataFilename << std::endl;
        return;
    }
    
    // 写入文件头，包含配置信息
    dataFile << "# 双摆模拟数据\n";
    dataFile << "# L1=" << config.L1 << " L2=" << config.L2 << "\n";
    dataFile << "# M1=" << config.M1 << " M2=" << config.M2 << "\n"; 
    dataFile << "# G=" << config.G << " dt=" << config.dt << "\n";
    dataFile << "# 数据格式: time x1 y1 x2 y2\n";
    
    std::cout << "开始双摆模拟并输出数据..." << std::endl;
    std::cout << "总步数: " << steps << std::endl;
    
    for (int i = 0; i < steps; i++) {
        if (i > 0) {  // 跳过第一步，因为需要old值
            verletStep();
        } else {
            // 第一步使用欧拉方法初始化
            double alpha1, alpha2;
            calculateAcceleration(alpha1, alpha2);
            theta1_old = theta1 - omega1 * config.dt + 0.5 * alpha1 * config.dt * config.dt;
            theta2_old = theta2 - omega2 * config.dt + 0.5 * alpha2 * config.dt * config.dt;
        }
        
        // 每100步输出一次数据
        if (i % 100 == 0) {
            Point p1 = getPendulum1Position();
            Point p2 = getPendulum2Position();
            dataFile << t << " " << p1.x << " " << p1.y << " " << p2.x << " " << p2.y << "\n";
        }
        
        t += config.dt;
    }
    
    dataFile.close();
    std::cout << "模拟完成！数据已保存到: " << dataFilename << std::endl;
}
