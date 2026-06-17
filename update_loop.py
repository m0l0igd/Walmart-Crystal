import time
import subprocess
import sys

def main():
    print("------------------------------------------------------------")
    print("🐾 Code Puppy static HTML live-loop engine started!")
    print("Runs build_crystal_portal.py every 30 seconds to rebuild index.html")
    print("Press CTRL+C in this terminal to stop the auto-rebuilder.")
    print("------------------------------------------------------------")
    
    try:
        while True:
            # Run the builder script
            subprocess.run([sys.executable, "build_crystal_portal.py"])
            
            # Sleep for 30 seconds
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🐾 Rebuild loop stopped. Stay loyal, Mike!")

if __name__ == "__main__":
    main()
