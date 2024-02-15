#ifndef VECTOR_PROCESSING_H
#define VECTOR_PROCESSING_H

#include <vector>
#include <nlohmann/json.hpp>
#include <cmath>

std::pair<std::vector<float>, std::vector<float>> extractVectors(const nlohmann::json &j)
{
    // Assuming j is a 2-element array of arrays, each inner array having 3 floats
    std::vector<float> vec1 = j[0].get<std::vector<float>>();
    std::vector<float> vec2 = j[1].get<std::vector<float>>();
    return {vec1, vec2};
}

std::pair<std::vector<float>, std::vector<float>> getAmpMean(const std::pair<std::vector<float>, std::vector<float>> &vectors)
{
    std::pair<std::vector<float>, std::vector<float>> amp_and_mean;
    for (int i = 0; i < 3; i++)
    {
        amp_and_mean.first.push_back((vectors.first[i] - vectors.second[i]) / 2.0f);
        amp_and_mean.second.push_back((vectors.first[i] + vectors.second[i]) / 2.0f);
    }
    return amp_and_mean;
}

std::vector<float> getMohrParams(const std::vector<float> &vector)
{
    float sg_x = vector[0];
    float sg_y = vector[1];
    float tau = vector[2];

    float dx = (sg_x - sg_y) / 2.0f;
    float dy = tau;

    float center = (sg_x + sg_y) / 2.0f;
    float radius = std::sqrt(std::pow(dx, 2) + std::pow(dy, 2));
    float phi_amp = std::atan2(dy, dx);

    return {center, radius, phi_amp};
}

#endif // VECTOR_PROCESSING_H
