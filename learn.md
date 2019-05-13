uiautomator:

pip install --upgrade --pre uiautomator2

pip install pillow

Install daemons to a device    电脑连接上一个手机或多个手机, 确保adb已经添加到环境变量中，执行下面的命令会自动安装本库所需要的设备端程序：uiautomator-server 、atx-agent、openstf/minicap、openstf/minitouch

init 所有的已经连接到电脑的设备
python -m uiautomator2 init


weditor:

github: https://github.com/openatx/weditor

## Installation
```
pip install -U weditor
```

## Usage

Create Shortcut in Desktop

```
python -m weditor --shortcut
```

By click shortcut or run in command line

```
python -m weditor
```


BatteryManager: https://blog.csdn.net/qq420290955/article/details/38800563
