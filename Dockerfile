# Use Alpine because it is tiny
FROM alpine:latest

# Install SSH and basic network tools
RUN apk add --no-cache openssh-server openssh-client iproute2 iputils

# Allow root login and set a password for SSH (for testing)
RUN echo 'administrator:root123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Generate SSH keys
RUN ssh-keygen -A

# Start the SSH service
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]