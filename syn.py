def read_img(img_path, target_size=(256, 256)):  
    return np.array(Image.open(img_path).resize(target_size)).astype("float32") / 255.  


def syn_low(img, img_gray, illumination_max=2.5, illumination_min=1.5, noise_max=0.03, noise_min=0.01):
    
    illumination = img_gray[:, :, np.newaxis]
    n = np.random.uniform(noise_min, noise_max)
    R = img / (illumination + 1e-7)
    exponent = np.random.uniform(illumination_min, illumination_max)
    L = (illumination + 1e-7) ** exponent
    return np.clip(R * L + np.random.normal(0, n, img.shape), 0, 1), exponent


def color_transfer_lab(clear, template, alpha_max = 1, alpha_min = 1):
    
    
    lab_a = cv2.cvtColor(np.float32(clear), cv2.COLOR_BGR2LAB)#.astype("float32")
    lab_b = cv2.cvtColor(np.float32(template), cv2.COLOR_BGR2LAB)#.astype("float32")
    
    l_a, a_a, b_a = cv2.split(lab_a)
    _, a_b, b_b = cv2.split(lab_b)
    
    def transfer_channel(channel_a, channel_b):
        mean_a, std_a = channel_a.mean(), channel_a.std()
        mean_b, std_b = channel_b.mean(), channel_b.std()
        return ((channel_a - mean_a) / std_a) * std_b + mean_b
    
    
    a_trans = transfer_channel(a_a, a_b)
    b_trans = transfer_channel(b_a, b_b)
    
    merged = cv2.merge([l_a, a_trans, b_trans])
    colored = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    
    gamma = np.random.rand(1) * (alpha_max - alpha_min) + alpha_min
    
    return clear * (1 - gamma) + colored * gamma, gamma


def syn_blur(img, depth, blurred, beta_max=3, beta_min=1):
    beta = np.random.rand(1) * (beta_max - beta_min) + beta_min
    remapped_depth = 0.3 + (1 - depth) * 0.4
    t = np.exp(-cv2.blur(remapped_depth,(22,22)) * beta)
    # t = np.exp(-remapped_depth * beta)
    
    return np.clip(img * t + blurred * (1 - t), 0, 1), beta

def estimate_A_highlight(I, top_percent=0.1, A_range=(0.6, 1.0)):
    luminance = np.mean(I, axis=2)
    threshold = np.percentile(luminance, 100 - top_percent * 100)
    highlight_pixels = I[luminance >= threshold]
    A_value = np.clip(np.mean(highlight_pixels), A_range[0], A_range[1])
    A = np.ones(3) * A_value
    return A


def syn_haze(img, depth, beta_max=3.0, beta_min=1.0, A_max=0.9, A_min=0.6):
    beta = np.random.rand(1) * (beta_max - beta_min) + beta_min
    remapped_depth = 0.3 + (1 - depth) * 0.4
    t = np.exp(-cv2.blur(remapped_depth,(22,22)) * beta)
    A = estimate_A_highlight(img)
    return np.clip(img * t + A * (1 - t), 0, 1), beta, A


def apply_degrade(clear, depth, blurred, temp, degrade_seq):
    out = clear.copy()

    if 'blur' in degrade_seq:
        out, _ = syn_blur(out, depth, blurred)

    if 'haze' in degrade_seq:
        out, _, _ = syn_haze(out, depth)

    if 'cast' in degrade_seq:
        out, _ = color_transfer_lab(out, temp)

    if 'low' in degrade_seq:
        gray = cv2.cvtColor(out.astype("float32"), cv2.COLOR_RGB2GRAY)
        out, _ = syn_low(out, gray)

    return out
