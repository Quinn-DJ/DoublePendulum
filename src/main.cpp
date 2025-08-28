#include "DoublePendulum.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    std::string configFile = "./config/config";
    std::string positionDataFile = "pendulum_data.txt";
    std::string angleDataFile = "pendulum_angles.txt";

    // Parse command line arguments
    if (argc >= 2) {
        configFile = argv[1];
    }
    if (argc >= 3) {
        positionDataFile = argv[2];
        // Generate angle data filename based on position data filename
        size_t lastDot = positionDataFile.find_last_of('.');
        if (lastDot != std::string::npos) {
            angleDataFile = positionDataFile.substr(0, lastDot) + "_angles" + positionDataFile.substr(lastDot);
        } else {
            angleDataFile = positionDataFile + "_angles";
        }
    }
    if (argc >= 4) {
        angleDataFile = argv[3];
    }
    
    try {
        // Load configuration
        Config config = DoublePendulum::loadConfig(configFile);

        // Create double pendulum object
        DoublePendulum pendulum(config);

        // Run simulation and output both position and angle data
        pendulum.simulateAndOutputAllData(positionDataFile, angleDataFile);
        
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
