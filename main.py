import aiohttp
import datetime
import os
import asyncio

import os
import datetime
import aiohttp
import asyncio

class AudioURLLoader:
    async def __call__(self, queue_data, stream_url, desired_duration):
        try:
            # Create a client session using aiohttp for making HTTP requests
            async with aiohttp.ClientSession() as session:
                # Send a GET request to the stream URL
                async with session.get(stream_url) as response:
                    # Open the file in binary append mode for writing the audio data
                    with open(queue_data["file_path"], 'ab') as f:
                        # Initialize variables to track duration and total length
                        start = datetime.datetime.now()
                        total_length = 0

                        # Iterate over the response content in chunks
                        async for chunk in response.content.iter_any():
                            # Write the chunk of audio data to the file
                            f.write(chunk)

                            # Update total length
                            total_length += len(chunk)

                            # Calculate the elapsed time since the start
                            elapsed_time = datetime.datetime.now() - start

                            # Print elapsed time and chunk size as reference
                            print(f"Elapsed Time: {elapsed_time}, Chunk Size: {len(chunk)}")

                            # Check if the desired duration is reached
                            if elapsed_time.total_seconds() >= desired_duration:
                                # If the desired duration is reached, break the loop
                                break
        except Exception as e:
            # If there is an exception during loading the audio data, log a warning
            print("PredictionAudioURLLoader error:", str(e))

# Create an instance of the loader
loader = AudioURLLoader()

# Specify the output file path and stream URL
folder_path = '/data'
stream_url = "https://go.webgateready.com/bondfm/"
target_start_time = datetime.datetime.strptime("12:38:00", "%H:%M:%S")
target_end_time = datetime.datetime.strptime("12:44:00", "%H:%M:%S")

async def run(target_start_time,target_end_time):
    while datetime.datetime.now().time() < target_end_time.time():
        # Generate a file name based on the current start time
        file_name = f"{target_start_time.strftime('%H%M%S')}.wav"
        file_path = os.path.join(folder_path, file_name)

        # Specify the desired duration in seconds (1 min and 20 sec)
        audio_lapse = 80

        # Run the loader to download the desired duration of audio
        await loader({"file_path": file_path}, stream_url, audio_lapse)

        # Add a delay of 10.42 seconds before processing the next stream
        await asyncio.sleep(10.42)

        # Move the start time forward by 1 minute (60 seconds)
        target_start_time += datetime.timedelta(seconds=audio_lapse)

asyncio.run(run(target_start_time,target_end_time))



