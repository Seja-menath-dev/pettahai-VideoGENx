from gradio_client import Client
import gradio as gr

# Initialize the client with your API key and the CogVideoX-5B-Space endpoint
api_key = "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"
client = Client("THUDM/CogVideoX-5B-Space", hf_token=api_key)

def generate_video(prompt, seed_value, scale_status, rife_status):
    result = client.predict(
        prompt=prompt,
        seed_value=seed_value,
        scale_status=scale_status,
        rife_status=rife_status,
        api_name="/generate"
    )
    
    video_url = result[0]['video']
    subtitles = result[0]['subtitles']
    video_file = result[1]
    gif_file = result[2]
    seed_used = result[3]
    
    # Save video file locally
    video_file_path = "generated_video.mp4"
    with open(video_file_path, "wb") as f:
        f.write(client.download_file(video_file))
    
    # Save GIF file locally
    gif_file_path = "generated_video.gif"
    with open(gif_file_path, "wb") as f:
        f.write(client.download_file(gif_file))
    
    return video_url, gif_file_path, seed_used

def enhance_prompt(prompt):
    enhanced_prompt = client.predict(
        prompt=prompt,
        api_name="/enhance_prompt_func"
    )
    return enhanced_prompt

def video_interface(prompt, seed_value=-1, scale_status=False, rife_status=False):
    video_url, gif_file_path, seed_used = generate_video(prompt, seed_value, scale_status, rife_status)
    return video_url, gif_file_path, seed_used

video_gen_interface = gr.Interface(
    fn=video_interface,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
        gr.Number(value=-1, label="Inference Seed (-1 for random)"),
        gr.Checkbox(label="Super-Resolution (720 × 480 -> 1440 × 960)"),
        gr.Checkbox(label="Frame Interpolation (8fps -> 16fps)")
    ],
    outputs=[
        gr.Video(label="Generated Video"),
        gr.File(label="Download GIF"),
        gr.Number(label="Seed Used for Video Generation")
    ],
    title="Pettah AI: VideoGenX"
)

def enhance_interface(prompt):
    enhanced_prompt = enhance_prompt(prompt)
    return enhanced_prompt

enhance_prompt_interface = gr.Interface(
    fn=enhance_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs=gr.Textbox(lines=2),
    title="Enhance Prompt with CogVideoX-5B"
)

if __name__ == "__main__":
    video_gen_interface.launch(share=True, server_port=5000)
    enhance_prompt_interface.launch(share=True, server_port=5000)
