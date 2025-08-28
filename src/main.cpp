#include "DoublePendulum.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    std::string configFile = "./config/config";
    std::string dataFile = "pendulum_data.txt";

    // Parse command line arguments
    if (argc >= 2) {
        configFile = argv[1];
    }
    if (argc >= 3) {
        dataFile = argv[2];
    }
    
    try {
        // Load configuration
        Config config = DoublePendulum::loadConfig(configFile);

        // Create double pendulum object
        DoublePendulum pendulum(config);

        // Run simulation and output data
        pendulum.simulateAndOutputData(dataFile);
        
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
