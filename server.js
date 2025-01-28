const image1 = "YOUR_IMAGE";
const image2 = "YOUR_IMAGE";
const image3 = "YOUR_IMAGE";
const image4 = "YOUR_IMAGE";

// API request payload
const payload = {
    messages: [
        {
            role: "user",
            content: [
                {
                    type: "text",
                    text:  ``,
                },
                {
                    type: "image_url",
                    image_url: { url: image1 },
                },
                {
                    type: "image_url",
                    image_url: { url: image2 },
                },
                {
                    type: "image_url",
                    image_url: { url: image3 },
                },
                {
                    type: "image_url",
                    image_url: { url: image4 },
                },
            ],
        },
    ],
};

// Make the API call
async function makeApiCall() {
    try {
        const response = await fetch(
            "https://<<YOUR_API>>/process_images",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response from server:", data);
    } catch (error) {
        console.error("Error making API call:", error.message);
    }
}

// Run the function
makeApiCall();
