# Mission configuration

initial_orbit = int(round(float(input("Enter current orbit (km): ")) * 1000)) # Convert to meters
final_orbit = int(round(float(input("Enter target orbit (km): ")) * 1000)) # Convert to meters

#Spacecraft parameters
#Thrust = float(input("Enter thrust (N): ")) # Thrust in Newtons
#Mass = float(input("Enter spacecraft mass (kg): ")) # Mass in kilograms

# Constants
μ_earth = 3.986e14 #m^3/s^2
r_earth = 6371000 #m