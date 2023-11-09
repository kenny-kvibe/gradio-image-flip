import gradio as gr
import numpy as np
import os


os.environ['GRADIO_ALLOW_FLAGGING'] = 'never'
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'

APP_TITLE = 'Gradio ⚡'
INITIAL_IMAGE = 'img/github_image.png'


def main() -> int:
	app = create_app()
	return run_app(app)


def process_flip_img(image:np.ndarray, colors_flip:bool, horizontal_flip:bool, vertical_flip:bool) -> np.ndarray:
	if vertical_flip:
		image = image[::-1]  # <= np.flipud(image) == np.flip(image, 1)
	if horizontal_flip:
		image = image[:, ::-1]  # <= np.fliplr(image) == np.flip(image, 0)
	if colors_flip:
		dtype_info = np.iinfo(image.dtype) if 'int' in image.dtype.name else np.finfo(image.dtype)
		img_depth = min(max(image.shape[2], 1), 3)
		image[:, :, :img_depth] = np.full(fill_value=dtype_info.max, shape=(*image.shape[:2], img_depth), dtype=image.dtype) - image[:, :, :img_depth]
	return image


def create_app(app_title:str = APP_TITLE) -> gr.Blocks:
	app_theme = gr.themes.Base(
		primary_hue=gr.themes.colors.sky,
		secondary_hue=gr.themes.colors.sky,
		neutral_hue=gr.themes.colors.neutral,
		font=('Segoe UI', 'Arial', 'DejaVu Sans', 'ui-sans-serif', 'system-ui', 'sans-serif'),
		font_mono=('Consolas', 'monospace'))

	with gr.Blocks(title=app_title, theme=app_theme) as app:
		inputs = []
		outputs = []

		gr.HTML(f'<h1 style="text-align:center">{app_title}</h1>', show_label=False)

		with gr.Row():
			with gr.Column(variant='panel'):
				inputs.append(gr.Image(
					INITIAL_IMAGE,
					type='numpy',
					sources=['upload'],
					image_mode='RGBA',
					show_label=False,
					show_share_button=False,
					show_download_button=False))

			with gr.Column(variant='panel'):
				outputs.append(gr.Image(
					type='numpy',
					sources=[],
					image_mode='RGBA',
					show_label=False,
					show_share_button=False,
					show_download_button=True))

		with gr.Row():
			with gr.Column():
				inputs.append(gr.Checkbox(label='Colors Flip (Image Negative)', value=True))
				inputs.append(gr.Checkbox(label='Horizontal Flip (Left–Right)', value=False))
				inputs.append(gr.Checkbox(label='Vertical Flip (Up–Down)', value=False))

		submit_btn = gr.Button(value='Run', variant='primary')
		submit_btn.click(fn=process_flip_img, inputs=inputs, outputs=outputs)

	return app


def run_app(app:gr.Blocks) -> int:
	app.launch(
		server_name='127.0.0.1',
		server_port=7860,
		share=False,
		debug=False,
		show_api=False,
		quiet=True)
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
