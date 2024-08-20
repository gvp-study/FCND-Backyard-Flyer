
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import utm



# Read the data from TLog.txt
with open('..\Logs\TLog.txt', 'r') as file:
    data = file.read()


def global_to_local(global_position, global_home):
    """
    Convert a global position (lon, lat, up) to a local position (north, east, down) relative to the home position.

    Returns:
        numpy array of the local position [north, east, down]
    """
    (east_home, north_home, _, _) = utm.from_latlon(global_home[1], global_home[0])
    (east, north, _, _) = utm.from_latlon(global_position[1], global_position[0])

    #local_position = np.array([north - north_home, east - east_home, -global_position[2]])
    local_position = [north - north_home, east - east_home, -global_position[2]]
    return local_position


def local_to_global(local_position, global_home):
    """
    Convert a local position (north, east, down) relative to the home position to a global position (lon, lat, up)

    Returns:
        numpy array of the global position [longitude, latitude, altitude]
    """
    (east_home, north_home, zone_number, zone_letter) = utm.from_latlon(global_home[1], global_home[0])
    (lat, lon) = utm.to_latlon(east_home + local_position[1], north_home + local_position[0], zone_number, zone_letter)

    lla = [lon, lat, -local_position[2]]
    return lla

# Initialize lists to store GLOBAL_POSITION and LOCAL_POSITION data
global_position = []
local_position = []
local_velocity = []
global_home = []

# Parse the data
for line in data.splitlines():
    parts = line.split(',')
    msg_id = parts[0]
    if msg_id == 'MsgID.GLOBAL_POSITION' and len(global_home) > 0:
        global_lat_lon = [float(parts[2]), float(parts[3]), float(parts[4])]
        local_NED = global_to_local(global_lat_lon, global_home)
        global_position.append(local_NED)
    elif msg_id == 'MsgID.GLOBAL_HOME':
        global_home = [float(parts[2]), float(parts[3]), float(parts[4])]
    elif msg_id == 'MsgID.LOCAL_POSITION':
        local_position.append([float(parts[2]), float(parts[3]), float(parts[4])])
    elif msg_id == 'MsgID.LOCAL_VELOCITY':
        local_velocity.append([float(parts[2]), float(parts[3]), float(parts[4])])

# Extract X, Y, Z coordinates for each position type
global_x, global_y, global_z = zip(*global_position)
local_x, local_y, local_z = zip(*local_position)
vel_x, vel_y, vel_z = zip(*local_velocity)

# Create a 3D subplot with 3 subplots side by side
fig = plt.figure(figsize=(18, 6))


# Plot GLOBAL_POSITION
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot(global_x, global_y, global_z, marker='o', linestyle='-', color='b')
ax1.set_title('GLOBAL_POSITION')
ax1.set_xlabel('North')
ax1.set_ylabel('East')
ax1.set_zlabel('Down')

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
