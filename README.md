### sms_emulator is a simple tool for emulating receiving and sending SMS messages by the end user.

To use it locally you have to make the following steps:
1. Install Docker and docker-compose.
2. Add your local user to Docker's group.
```bash
sudo usermod -aG docker $USER
```
3. Clone project
```bash
git clone git@github.com:Alliera/sms_emulator.git
```
4. Go to `demo_deployment`
```bash
cd sms_emulator/demo_deployment
```
5. Run build.sh script to create Docker containers
```
build.sh
```
6. Press Ctrl-Z to detach output and go to http://localhost:9000
