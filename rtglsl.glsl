#version 300 es

precision highp float;

out vec4 FragColor;
in vec2 TexCoord;

uniform vec3 cameraPos;
uniform vec3 cameraDir;
uniform vec3 cameraUp;
uniform vec3 cameraRight;
uniform float aspectRatio;
uniform float fov;
uniform int maxDepth;
uniform int samplesPerPixel;
uniform vec2 textureSize;

struct Ray {
    vec3 orig;
    vec3 dir;
};

struct HitRecord {
    vec3 p;
    vec3 normal;
    float t;
    bool frontFace;
    vec3 color;
    int materialType;
    float fuzz;
    float refIdx;
};

struct Sphere {
    vec3 center;
    float radius;
    vec3 color;
    int materialType; // 0: Lambertian, 1: Metal, 2: Dielectric
    float fuzz; // Only for Metal
    float refIdx; // Only for Dielectric
};

#define MAX_SPHERES 10
uniform Sphere spheres[MAX_SPHERES];
uniform int numSpheres;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

vec3 randomInUnitSphere() {
    vec3 p;
    do {
        p = 2.0 * vec3(random(gl_FragCoord.xy), random(gl_FragCoord.xy + vec2(1.0, 0.0)), random(gl_FragCoord.xy + vec2(0.0, 1.0))) - vec3(1.0);
    } while (dot(p, p) >= 1.0);
    return p;
}

vec3 myReflect(vec3 v, vec3 n) {
    return v - 2.0 * dot(v, n) * n;
}

bool myRefract(vec3 v, vec3 n, float niOverNt, out vec3 refracted) {
    vec3 uv = normalize(v);
    float dt = dot(uv, n);
    float discriminant = 1.0 - niOverNt * niOverNt * (1.0 - dt * dt);
    if (discriminant > 0.0) {
        refracted = niOverNt * (uv - n * dt) - n * sqrt(discriminant);
        return true;
    }
    return false;
}

float schlick(float cosine, float refIdx) {
    float r0 = (1.0 - refIdx) / (1.0 + refIdx);
    r0 = r0 * r0;
    return r0 + (1.0 - r0) * pow((1.0 - cosine), 5.0);
}

bool hitSphere(Sphere sphere, Ray ray, float tMin, float tMax, out HitRecord rec) {
    vec3 oc = ray.orig - sphere.center;
    float a = dot(ray.dir, ray.dir);
    float b = dot(oc, ray.dir);
    float c = dot(oc, oc) - sphere.radius * sphere.radius;
    float discriminant = b * b - a * c;
    if (discriminant > 0.0) {
        float temp = (-b - sqrt(discriminant)) / a;
        if (temp < tMax && temp > tMin) {
            rec.t = temp;
            rec.p = ray.orig + rec.t * ray.dir;
            rec.normal = (rec.p - sphere.center) / sphere.radius;
            rec.color = sphere.color;
            rec.frontFace = dot(ray.dir, rec.normal) < 0.0;
            if (!rec.frontFace) rec.normal = -rec.normal;
            rec.materialType = sphere.materialType;
            rec.fuzz = sphere.fuzz;
            rec.refIdx = sphere.refIdx;
            return true;
        }
        temp = (-b + sqrt(discriminant)) / a;
        if (temp < tMax && temp > tMin) {
            rec.t = temp;
            rec.p = ray.orig + rec.t * ray.dir;
            rec.normal = (rec.p - sphere.center) / sphere.radius;
            rec.color = sphere.color;
            rec.frontFace = dot(ray.dir, rec.normal) < 0.0;
            if (!rec.frontFace) rec.normal = -rec.normal;
            rec.materialType = sphere.materialType;
            rec.fuzz = sphere.fuzz;
            rec.refIdx = sphere.refIdx;
            return true;
        }
    }
    return false;
}

bool scatter(Ray rayIn, HitRecord rec, out vec3 attenuation, out Ray scattered) {
    if (rec.materialType == 0) { // Lambertian
        vec3 target = rec.p + rec.normal + randomInUnitSphere();
        scattered = Ray(rec.p, target - rec.p);
        attenuation = rec.color;
        return true;
    } else if (rec.materialType == 1) { // Metal
        vec3 reflected = myReflect(normalize(rayIn.dir), rec.normal);
        scattered = Ray(rec.p, reflected + rec.fuzz * randomInUnitSphere());
        attenuation = rec.color;
        return dot(scattered.dir, rec.normal) > 0.0;
    } else if (rec.materialType == 2) { // Dielectric
        vec3 outwardNormal;
        vec3 reflected = myReflect(rayIn.dir, rec.normal);
        float niOverNt;
        attenuation = vec3(1.0);
        vec3 refracted;
        float reflectProb;
        float cosine;
        if (dot(rayIn.dir, rec.normal) > 0.0) {
            outwardNormal = -rec.normal;
            niOverNt = rec.refIdx;
            cosine = rec.refIdx * dot(rayIn.dir, rec.normal) / length(rayIn.dir);
        } else {
            outwardNormal = rec.normal;
            niOverNt = 1.0 / rec.refIdx;
            cosine = -dot(rayIn.dir, rec.normal) / length(rayIn.dir);
        }
        if (myRefract(rayIn.dir, outwardNormal, niOverNt, refracted)) {
            reflectProb = schlick(cosine, rec.refIdx);
        } else {
            reflectProb = 1.0;
        }
        if (random(gl_FragCoord.xy) < reflectProb) {
            scattered = Ray(rec.p, reflected);
        } else {
            scattered = Ray(rec.p, refracted);
        }
        return true;
    }
    return false;
}

vec3 rayColor(Ray ray, int depth) {
    HitRecord rec;
    if (depth <= 0) {
        return vec3(0.0);
    }
    for (int i = 0; i < numSpheres; i++) {
        if (hitSphere(spheres[i], ray, 0.001, 1000.0, rec)) {
            Ray scattered;
            vec3 attenuation;
            if (scatter(ray, rec, attenuation, scattered)) {
                return attenuation * rayColor(scattered, depth - 1);
            }
            return vec3(0.0);
        }
    }
    vec3 unitDirection = normalize(ray.dir);
    float t = 0.5 * (unitDirection.y + 1.0);
    return (1.0 - t) * vec3(1.0) + t * vec3(0.5, 0.7, 1.0);
}

Ray getRay(vec2 uv) {
    vec3 lowerLeftCorner = cameraPos - cameraRight * aspectRatio * tan(radians(fov) / 2.0) - cameraUp * tan(radians(fov) / 2.0) - cameraDir;
    vec3 horizontal = 2.0 * cameraRight * aspectRatio * tan(radians(fov) / 2.0);
    vec3 vertical = 2.0 * cameraUp * tan(radians(fov) / 2.0);
    vec3 direction = lowerLeftCorner + uv.x * horizontal + uv.y * vertical - cameraPos;
    return Ray(cameraPos, direction);
}

void main() {
    vec3 color = vec3(0.0);
    for (int s = 0; s < samplesPerPixel; s++) {
        vec2 uv = TexCoord + vec2(random(gl_FragCoord.xy), random(gl_FragCoord.xy + vec2(1.0, 0.0))) / textureSize;
        Ray ray = getRay(uv);
        color += rayColor(ray, maxDepth);
    }
    color /= float(samplesPerPixel);
    color = sqrt(color); // Gamma correction
    FragColor = vec4(color, 1.0);
}