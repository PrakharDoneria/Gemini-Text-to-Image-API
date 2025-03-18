# **Gemini Text-to-Image API**  

This API allows you to generate images using Google Gemini API and upload them directly to ImgBB without saving them locally.  

## **Base URL**  
```
https://gemini-text-to-image-api.vercel.app/
```

## **Endpoint**  
### **POST /generate**  
Generates an image from text and returns the image URL.  

### **Request Parameters (JSON Body)**  
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The text prompt for image generation |
| `api` | string | Yes | Your Google Gemini API key |

### **Example Request**  
```bash
curl -X POST "https://gemini-text-to-image-api.vercel.app/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "A futuristic car on Mars",
           "api": "your_gemini_api_key"
         }'
```

### **Example Response**  
```json
{
    "image_url": "https://i.ibb.co/example.jpg"
}
```

## **Setup (For Local Deployment)**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/gemini-text-to-image-api.git
   cd gemini-text-to-image-api
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:  
   ```bash
   export IMGBB_API_KEY="your_imgbb_api_key"
   ```
4. Run the Flask server:  
   ```bash
   python main.py
   ```