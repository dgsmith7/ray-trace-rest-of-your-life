    #version 300 es
    
    precision mediump float;
    
    in vec2 vTexCoord;
    uniform vec2 u_resolution;
    out vec4 fColor;
    const vec3 LUMCOEFFS = vec3( 0.2125,0.7154,0.0721 );
    const float PI = 3.1415926535;

    float aspectRatio = 16.0 / 9.0; // Ratio of image width over height
    int imagWidth = 1200; // Rendered image width in pixel count
    int imageHeight = max(int(imageWidth / aspectRatio), 1);
    int samplesPerPixel = 10; // Count of random samples for each pixel
    int maxDepth = 10; # Maximum number of ray bounces into scene.  Keep below 48.
    int vfov = 35; // Vertical view angle (field of view)
    float theta = radians(vfov);
    float h = tan(theta/2.0);
    vec3 lookFrom = vec3(7, 5, 7);
    vec3 center = lookFrom;
    vec3 lookAt = vec3(0, 2, 0);
    vec3 vUp = vec3(0, 1, 0);
    float defocus_angle = 0.0;
    float focusDist = 10.0;
    float viewportHeight = 2.0 * h * focusDist;
    float viewportWidth = viewportHeight * (imageWidth / imageHeight);
    vec3 w = normalize(lookFrom - lookAt);
    vec3 u = normalize(cross(vUp, w));
    vec3 v = cross(w, u);
    vec3 viewportU = viewportWidth * u;
    vec3 viewportV = viewportHeight * -v;
    vec3 pixelDeltaU = viewportU / imageWidth;
    vec3 pixelDeltaV = viewportV / imageHeight;
    vec3 viewportUpperLeft = center - (focusDist * w) - (viewportU/2.0) - (viewportV/2.0);
    vec3 pixel00_loc = viewportUpperLeft + 0.5 * (pixelDeltaU + pixelDeltaV);
    # Calculate the defouc disk basis vectors
    float defocusRadius = focusDist * tan(radians(defocusAngle / 2.0));
    float defocusDisk_u = u * defocusRadius;
    float defocusDisk_v = v * defocusRadius;

init() {
}

metal() {}

lambert() {}

dielectric() {}

render() {}

rayColor() {}

sampleSquare() {}

defocusDiskSample() {}

getRay() {}

main() {

  fColor = vec3(0.0, 0.0, 1.0)
}