
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Read the data from TLog.txt 
with open('..\Logs\TLog.txt', 'r') as file:
    data = file.read()


# Initialize lists to store GLOBAL_POSITION and LOCAL_POSITION data
global_position = []
local_position = []
local_velocity = []

# Parse the data
for line in data.splitlines():
    parts = line.split(',')
    msg_id = parts[0]
    if msg_id == 'MsgID.GLOBAL_POSITION':
        global_position.append([float(parts[2]), float(parts[3]), float(parts[4]), float(parts[4])])
    elif msg_id == 'MsgID.LOCAL_POSITION':
        local_position.append([float(parts[2]), float(parts[3]), float(parts[4]), float(parts[4])])
    elif msg_id == 'MsgID.LOCAL_VELOCITY':
        local_velocity.append([float(parts[2]), float(parts[3]), float(parts[4]), float(parts[4])])

# Extract X, Y, Z coordinates for each position type
global_x, global_y, global_z, _ = zip(*global_position)
local_x, local_y, local_z, _ = zip(*local_position)
vel_x, vel_y, vel_z, _ = zip(*local_velocity)

# Create a 3D subplot with 3 subplots side by side
fig = plt.figure(figsize=(18, 6))


# Plot GLOBAL_POSITION
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot(global_x, global_y, global_z, marker='o', linestyle='-', color='b')
ax1.set_title('GLOBAL_POSITION')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.set_zlabel('Altitude')

# Plot LOCAL_POSITION
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot(local_x, local_y, local_z, marker='o', linestyle='-', color='r')
ax2.set_title('LOCAL_POSITION')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

# Plot LOCAL_VELOCITY
ax3 = fig.add_subplot(133, projection='3d')
ax3.plot(vel_x, vel_y, vel_z, marker='o', linestyle='-', color='g')
ax3.set_title('LOCAL_VELOCITY')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')

# Show the plots
plt.show()


