This is a Python port of a favorite project of mine, whose function is to create fake Craigslist Free listings and post them in the NYC area, every day.  The crux of the project is the unreliable outputs of early gpt(gpt-2), which myself and many others were exposed to thanks to the outstanding work of @minimaxir and his iterations of Python libraries, which made early LMs available and easier to understand. 

Prior versions sprawled out in separate Ruby/Rails, Javascript, and Python scripts, interacted via a local network cast by ngrok, and even looped in Twilio API calls which allowed me to punch in by text message, keeping me entertained at my barista job.

The only concession I plan to make to advances in AI development since is image generation based on the post title--I want to keep thing loose and weird.

What you see here is simple code using the GMail API to manuever around some site spam protections, and Playwright instances to handle the post automation.  On the back end of things is a separate project that utilizes scraped data to train a language model using @minimaxir's gpt-2-simple and write outputs to files that the parser can read.