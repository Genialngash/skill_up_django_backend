import {useState, useEffect} from 'react';
import {getRemainingTimeUntilMsTimestamp} from './CountdownTimerUtils';

const defaultRemainingTime = {
    seconds: '00',
    minutes: '00',
    hours: '00',
    days: '00'
}

const CountdownTimer = ({countdownTimestampMs}) => {
    const [remainingTime, setRemainingTime] = useState(defaultRemainingTime);

    useEffect(() => {
        const intervalId = setInterval(() => {
            updateRemainingTime(countdownTimestampMs);
        }, 1000);
        return () => clearInterval(intervalId);
    },[countdownTimestampMs]);

    function updateRemainingTime(countdown) {
        setRemainingTime(getRemainingTimeUntilMsTimestamp(countdown));
    }

    return(
        <div className="countdown-timer flex-wrap mb-2 font-46">
        <div>
          <span> {remainingTime.days}</span>
          <span>days</span>
        </div>
  
        <div>
          <span>{remainingTime.hours}</span>
          <span>hours</span>
        </div>
  
        <div>
          <span>{remainingTime.minutes}</span> <span>minutes</span>
        </div>
  
        <div>
          <span>{remainingTime.seconds}</span> <span>seconds</span>{" "}
        </div>
      </div>
    );
}

export default CountdownTimer;