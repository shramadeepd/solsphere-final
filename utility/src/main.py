import time
import signal
import sys
from utils import system_checks, api_client, state_manager, logger, config

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global running
    logger.logger.info(f"Received signal {signum}, shutting down gracefully...")
    running = False

def main():
    """Main function for the system utility."""
    global running
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.logger.info("System Utility starting...")
    
    # Test backend connection
    if not api_client.test_connection():
        logger.logger.warning("Backend connection test failed. Continuing anyway...")
    
    # Send initial report
    try:
        logger.logger.info("Collecting initial system information...")
        initial_state = system_checks.collect_system_info()
        
        if initial_state.get("overall_status") == "error":
            logger.logger.error("Failed to collect initial system information")
            return 1
        
        logger.logger.info("Sending initial report...")
        if api_client.send_report(initial_state):
            logger.logger.info("Initial report sent successfully")
            state_manager.save_state(initial_state)
        else:
            logger.logger.warning("Failed to send initial report")
    
    except Exception as e:
        logger.logger.error(f"Error during initialization: {str(e)}")
        return 1
    
    logger.logger.info(f"Starting monitoring loop (check interval: {config.CHECK_INTERVAL_MINUTES} minutes)")
    
    try:
        while running:
            try:
                # Collect current system information
                current_state = system_checks.collect_system_info()
                
                if current_state.get("overall_status") == "error":
                    logger.logger.error("Failed to collect system information")
                    time.sleep(config.CHECK_INTERVAL_MINUTES * 60)
                    continue
                
                # Load last state for comparison
                last_state = state_manager.load_last_state()
                
                # Check if state has changed
                if state_manager.has_state_changed(current_state, last_state):
                    logger.logger.info("System state changes detected, sending report...")
                    
                    if api_client.send_report(current_state):
                        logger.logger.info("Report sent successfully")
                        state_manager.save_state(current_state)
                    else:
                        logger.logger.error("Failed to send report")
                else:
                    logger.logger.debug("No system state changes detected")
                
                # Log system health summary
                overall_status = current_state.get("overall_status", "unknown")
                issues_count = len(current_state.get("issues", []))
                
                if overall_status == "healthy":
                    logger.logger.info(f"System health: {overall_status}")
                elif overall_status == "unhealthy":
                    logger.logger.warning(f"System health: {overall_status} ({issues_count} issues)")
                else:
                    logger.logger.info(f"System health: {overall_status}")
                
                # Wait for next check
                logger.logger.debug(f"Waiting {config.CHECK_INTERVAL_MINUTES} minutes until next check...")
                time.sleep(config.CHECK_INTERVAL_MINUTES * 60)
                
            except KeyboardInterrupt:
                logger.logger.info("Interrupted by user")
                break
            except Exception as e:
                logger.logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(config.CHECK_INTERVAL_MINUTES * 60)
    
    finally:
        logger.logger.info("System Utility stopped")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
