#ifndef DOUBLE_PENDULUM_HPP
#define DOUBLE_PENDULUM_HPP

#include <vector>
#include <string>
#include <cmath>

struct Config {
    double L1, L2;       // Pendulum lengths
    double M1, M2;       // Masses
    double G;            // Gravitational acceleration
    double theta1, theta2;   // Initial angles
    double omega1, omega2;   // Initial angular velocities
    double dt;           // Time step
    double totalTime;    // Total simulation time
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
    
    // Normalize angle to [-π, π] range
    double normalizeAngle(double angle);
    
public:
    DoublePendulum(const Config& cfg);
    
    // Load configuration file
    static Config loadConfig(const std::string& filename);
    
    // Calculate next step using Verlet algorithm
    void verletStep();
    
    // Calculate acceleration
    void calculateAcceleration(double& alpha1, double& alpha2);
    
    // Run simulation and output data to file
    void simulateAndOutputData(const std::string& dataFilename);
    
    // Run simulation and output both position and angle data
    void simulateAndOutputAllData(const std::string& positionFilename, const std::string& angleFilename);
    
    // Get ball positions
    Point getPendulum1Position();
    Point getPendulum2Position();
    
    // Get current angles
    double getTheta1() const { return theta1; }
    double getTheta2() const { return theta2; }
};

#endif
