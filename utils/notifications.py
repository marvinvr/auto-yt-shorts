import logging
import traceback

import apprise

logger = logging.getLogger(__name__)


def send_error_notification(error_message: str, exception: Exception = None, context: str = ""):
    """
    Send error notification via Apprise.
    
    Args:
        error_message: Human-readable error message
        exception: Optional exception object for detailed error info
        context: Optional context information (e.g., "Video Generation", "Credential Update")
    """
    try:
        from config import APPRISE_URL
        
        if not APPRISE_URL:
            logger.warning("APPRISE_URL not configured, skipping error notification")
            logger.error(error_message)
            logger.exception(exception)
            return
            
        # Create Apprise instance
        apobj = apprise.Apprise()
        apobj.add(APPRISE_URL)
        
        # Build notification content
        title = f"Auto YT Shorts Error"
        if context:
            title += f" - {context}"
            
        body = f"Error: {error_message}\n"
        
        if exception:
            body += f"\nException: {str(exception)}\n"
            body += f"\nTraceback:\n{traceback.format_exc()}"
        
        # Send notification
        success = apobj.notify(
            body=body,
            title=title
        )
        
        if success:
            logger.info("Error notification sent successfully")
        else:
            logger.warning("Failed to send error notification")
            
    except Exception as e:
        logger.error(f"Failed to send error notification: {e}")


def send_success_notification(message: str, context: str = ""):
    """
    Send success notification via Apprise.
    
    Args:
        message: Success message
        context: Optional context information
    """
    try:
        from config import APPRISE_URL, NOTIFY_ON_SUCCESS
        
        if not APPRISE_URL:
            return
            
        if not NOTIFY_ON_SUCCESS:
            logger.info(f"Success notification skipped (NOTIFY_ON_SUCCESS=False): {message}")
            return
            
        # Create Apprise instance
        apobj = apprise.Apprise()
        apobj.add(APPRISE_URL)
        
        # Build notification content
        title = f"Auto YT Shorts Success"
        if context:
            title += f" - {context}"
        
        # Send notification
        success = apobj.notify(
            body=message,
            title=title
        )
        
        if success:
            logger.info("Success notification sent successfully")
        else:
            logger.warning("Failed to send success notification")
            
    except Exception as e:
        logger.error(f"Failed to send success notification: {e}")