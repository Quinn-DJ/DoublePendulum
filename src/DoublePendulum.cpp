#include "DoublePendulum.hpp"
#include <iostream>
#include <fstream>
#include <sstream>

DoublePendulum::DoublePendulum(const Config& cfg) : config(cfg) {
    theta1 = normalizeAngle(config.theta1);
    theta2 = normalizeAngle(config.theta2);
    omega1 = config.omega1;
    omega2 = config.omega2;

    // Initialize old values for Verlet algorithm
    theta1_old = theta1;
    theta2_old = theta2;
    omega1_old = omega1;
    omega2_old = omega2;
}

double DoublePendulum::normalizeAngle(double angle) {
    // Normalize angle to [-π, π] range
    while (angle > M_PI) angle -= 2 * M_PI;
    while (angle < -M_PI) angle += 2 * M_PI;
    return angle;
}

Config DoublePendulum::loadConfig(const std::string& filename) {
    Config cfg;
    std::ifstream file(filename);
    std::string line;
    
    if (!file.is_open()) {
        std::cerr << "Cannot open config file: " << filename << std::endl;
        // Set default values
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
        // Skip comments and empty lines
        if (line.empty() || line[0] == '#') continue;
        
        size_t pos = line.find('=');
        if (pos == std::string::npos) continue;
        
        std::string key = line.substr(0, pos);
        std::string value = line.substr(pos + 1);
        
        // Remove inline comments
        size_t comment_pos = value.find('#');
        if (comment_pos != std::string::npos) {
            value = value.substr(0, comment_pos);
        }
        
        // Remove leading and trailing whitespace
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
    
    // Check for numerical stability - prevent division by very small numbers
    const double MIN_DENOM = 1e-10;
    if (std::abs(denom1) < MIN_DENOM) {
        // Use a small but non-zero value to prevent explosion
        denom1 = (denom1 >= 0) ? MIN_DENOM : -MIN_DENOM;
    }
    if (std::abs(denom2) < MIN_DENOM) {
        denom2 = (denom2 >= 0) ? MIN_DENOM : -MIN_DENOM;
    }
    
    // Calculate angular acceleration of first pendulum
    alpha1 = (-M2 * L1 * omega1 * omega1 * sin_delta * cos_delta
              + M2 * g * sin(theta2) * cos_delta
              + M2 * L2 * omega2 * omega2 * sin_delta
              - (M1 + M2) * g * sin(theta1)) / denom1;
    
    // Calculate angular acceleration of second pendulum
    alpha2 = (-M2 * L2 * omega2 * omega2 * sin_delta * cos_delta
              + (M1 + M2) * g * sin(theta1) * cos_delta
              + (M1 + M2) * L1 * omega1 * omega1 * sin_delta
              - (M1 + M2) * g * sin(theta2)) / denom2;
    
    // Clamp accelerations to prevent runaway values
    const double MAX_ACCEL = 1000.0;  // Reasonable upper bound
    alpha1 = std::max(-MAX_ACCEL, std::min(MAX_ACCEL, alpha1));
    alpha2 = std::max(-MAX_ACCEL, std::min(MAX_ACCEL, alpha2));
}

/*
 * Verlet Integration Algorithm Implementation
 * ==========================================
 * 
 * The Verlet algorithm is a numerical method for integrating equations of motion.
 * It provides better stability and energy conservation compared to Euler methods.
 * 
 * Position update formula:
 *   $\theta(t+\Delta t) = 2\theta(t) - \theta(t-\Delta t) + \alpha(t)(\Delta t)^2$
 * 
 * Velocity calculation (central difference):
 *   $\omega(t) = \frac{\theta(t+\Delta t) - \theta(t-\Delta t)}{2\Delta t}$
 * 
 * Where:
 *   $\theta$ = angular position
 *   $\omega$ = angular velocity  
 *   $\alpha$ = angular acceleration
 *   $\Delta t$ = time step
 */

void DoublePendulum::verletStep() {
    double alpha1, alpha2;
    calculateAcceleration(alpha1, alpha2);
    
    // Update positions using Verlet algorithm
    // Mathematical formula: $\theta(t+\Delta t) = 2\theta(t) - \theta(t-\Delta t) + \alpha(t)(\Delta t)^2$
    // where $\alpha(t)$ is the angular acceleration at time $t$
    double theta1_new = 2 * theta1 - theta1_old + alpha1 * config.dt * config.dt;
    double theta2_new = 2 * theta2 - theta2_old + alpha2 * config.dt * config.dt;
    
    // Update angular velocities (using central difference)
    // Mathematical formula: $\omega(t) = \frac{\theta(t+\Delta t) - \theta(t-\Delta t)}{2\Delta t}$
    // This provides better numerical stability than forward/backward differences
    omega1 = (theta1_new - theta1_old) / (2 * config.dt);
    omega2 = (theta2_new - theta2_old) / (2 * config.dt);
    
    // Update positions
    theta1_old = theta1;
    theta2_old = theta2;
    theta1 = normalizeAngle(theta1_new);
    theta2 = normalizeAngle(theta2_new);
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
    
    // Open data output file
    std::ofstream dataFile(dataFilename);
    if (!dataFile.is_open()) {
        std::cerr << "Cannot create data file: " << dataFilename << std::endl;
        return;
    }
    
    // Write file header with configuration information
    dataFile << "# Double Pendulum Simulation Data\n";
    dataFile << "# L1=" << config.L1 << " L2=" << config.L2 << "\n";
    dataFile << "# M1=" << config.M1 << " M2=" << config.M2 << "\n"; 
    dataFile << "# G=" << config.G << " dt=" << config.dt << "\n";
    dataFile << "# Data format: time x1 y1 x2 y2\n";
    
    // Progress tracking variables
    int lastReportedProgress = -1;
    
    std::cout << "Starting simulation..." << std::endl;
    std::cout << "Total steps: " << steps << std::endl;
    
    for (int i = 0; i < steps; i++) {
        // Calculate and display progress percentage
        int currentProgress = static_cast<int>((i * 100.0) / steps);
        if (currentProgress > lastReportedProgress) {
            lastReportedProgress = currentProgress;
            // std::cout << "\rProgress: " << currentProgress << "%" << std::flush;
        }
        
        if (i > 0) {  // Skip first step as it needs old values
            verletStep();
        } else {
            // First step uses Euler method for initialization
            // Mathematical formula: $\theta(t-\Delta t) = \theta(t) - \omega(t)\Delta t + \frac{1}{2}\alpha(t)(\Delta t)^2$
            // This provides the "old" position needed for Verlet algorithm
            double alpha1, alpha2;
            calculateAcceleration(alpha1, alpha2);
            theta1_old = theta1 - omega1 * config.dt + 0.5 * alpha1 * config.dt * config.dt;
            theta2_old = theta2 - omega2 * config.dt + 0.5 * alpha2 * config.dt * config.dt;
        }
        
        // Output data every 100 steps
        if (i % 100 == 0) {
            Point p1 = getPendulum1Position();
            Point p2 = getPendulum2Position();
            dataFile << t << " " << p1.x << " " << p1.y << " " << p2.x << " " << p2.y << "\n";
        }
        
        t += config.dt;
    }
    
    // Display completion message
    std::cout << "\rProgress: 100%" << std::endl;
    std::cout << "Simulation completed! Data saved to: " << dataFilename << std::endl;
    
    dataFile.close();
}

void DoublePendulum::simulateAndOutputAllData(const std::string& positionFilename, const std::string& angleFilename) {
    double t = 0.0;
    int steps = static_cast<int>(config.totalTime / config.dt);
    
    // Open data output files
    std::ofstream positionFile(positionFilename);
    std::ofstream angleFile(angleFilename);
    
    if (!positionFile.is_open()) {
        std::cerr << "Cannot create position file: " << positionFilename << std::endl;
        return;
    }
    
    if (!angleFile.is_open()) {
        std::cerr << "Cannot create angle file: " << angleFilename << std::endl;
        return;
    }
    
    // Write file headers with configuration information
    positionFile << "# Double Pendulum Simulation Data - Positions\n";
    positionFile << "# L1=" << config.L1 << " L2=" << config.L2 << "\n";
    positionFile << "# M1=" << config.M1 << " M2=" << config.M2 << "\n"; 
    positionFile << "# G=" << config.G << " dt=" << config.dt << "\n";
    positionFile << "# Data format: time x1 y1 x2 y2\n";
    
    angleFile << "# Double Pendulum Simulation Data - Angles\n";
    angleFile << "# L1=" << config.L1 << " L2=" << config.L2 << "\n";
    angleFile << "# M1=" << config.M1 << " M2=" << config.M2 << "\n"; 
    angleFile << "# G=" << config.G << " dt=" << config.dt << "\n";
    angleFile << "# Data format: time theta1 theta2\n";
    
    // Progress tracking variables
    int lastReportedProgress = -1;
    
    std::cout << "Starting simulation..." << std::endl;
    std::cout << "Total steps: " << steps << std::endl;
    
    for (int i = 0; i < steps; i++) {
        // Calculate and display progress percentage
        int currentProgress = static_cast<int>((i * 100.0) / steps);
        if (currentProgress > lastReportedProgress) {
            lastReportedProgress = currentProgress;
            // std::cout << "\rProgress: " << currentProgress << "%" << std::flush;
        }
        
        if (i > 0) {  // Skip first step as it needs old values
            verletStep();
        } else {
            // First step uses Euler method for initialization
            // Mathematical formula: $\theta(t-\Delta t) = \theta(t) - \omega(t)\Delta t + \frac{1}{2}\alpha(t)(\Delta t)^2$
            // This provides the "old" position needed for Verlet algorithm
            double alpha1, alpha2;
            calculateAcceleration(alpha1, alpha2);
            theta1_old = theta1 - omega1 * config.dt + 0.5 * alpha1 * config.dt * config.dt;
            theta2_old = theta2 - omega2 * config.dt + 0.5 * alpha2 * config.dt * config.dt;
        }
        
        // Output data every 100 steps
        if (i % 100 == 0) {
            Point p1 = getPendulum1Position();
            Point p2 = getPendulum2Position();
            positionFile << t << " " << p1.x << " " << p1.y << " " << p2.x << " " << p2.y << "\n";
            angleFile << t << " " << theta1 << " " << theta2 << "\n";
        }
        
        t += config.dt;
    }
    
    // Display completion message
    std::cout << "\rProgress: 100%" << std::endl;
    std::cout << "Simulation completed!" << std::endl;
    std::cout << "Position data saved to: " << positionFilename << std::endl;
    std::cout << "Angle data saved to: " << angleFilename << std::endl;
    
    positionFile.close();
    angleFile.close();
}
