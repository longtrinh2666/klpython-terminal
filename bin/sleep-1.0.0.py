author = "longtrinh2666"
import time

def register(commands, ENV):
    def sleep_cmd(args):
        """
        Delay execution for a specified amount of time.
        Usage: sleep <time>[s|m|h]
        Example: sleep 5s, sleep 2m, sleep 1.5h
        """
        if not args:
            print("Usage: sleep <time>[s|m|h]")
            return

        raw_arg = args[0].strip().lower()
        
        try:
            multiplier = 1.0  # Mặc định tính bằng giây (seconds)
            
            # Xử lý các hậu tố s, m, h
            if raw_arg.endswith("s"):
                multiplier = 1.0
                raw_arg = raw_arg[:-1]
            elif raw_arg.endswith("m"):
                multiplier = 60.0
                raw_arg = raw_arg[:-1]
            elif raw_arg.endswith("h"):
                multiplier = 3600.0
                raw_arg = raw_arg[:-1]

            # Chuyển đổi phần số sang kiểu float
            sec = float(raw_arg) * multiplier
            
            if sec < 0:
                print("E: Time cannot be negative")
                return

            time.sleep(sec)
            
        except ValueError:
            print("E: Invalid time format. Use numbers with optional suffix s, m, or h (e.g., 5s, 2m)")
        except KeyboardInterrupt:
            print("\nSleep interrupted")

    # Đăng ký lệnh 'sleep' vào hệ thống commands của terminal
    commands["sleep"] = sleep_cmd