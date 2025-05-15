// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#pragma once

#include <cstddef>
#include <mutex>
#include <vector>
#include "utils.h"

namespace diskann
{

struct Neighbor
{
    unsigned id;
    float distance;
    bool expanded;

    Neighbor() = default;

    Neighbor(unsigned id, float distance) : id{id}, distance{distance}, expanded(false)
    {
    }

    inline bool operator<(const Neighbor &other) const
    {
        return distance < other.distance || (distance == other.distance && id < other.id);
    }

    inline bool operator==(const Neighbor &other) const
    {
        return (id == other.id);
    }
};

// Invariant: after every `insert` and `closest_unexpanded()`, `_cur` points to
//            the first Neighbor which is unexpanded.
class NeighborPriorityQueue
{
  public:
    NeighborPriorityQueue() : _size(0), _capacity(0), _cur(0)
    {
    }

    explicit NeighborPriorityQueue(size_t capacity) : _size(0), _capacity(capacity), _cur(0), _data(capacity + 1)
    {
    }

    // Inserts the item ordered into the set up to the sets capacity.
    // The item will be dropped if it is the same id as an exiting
    // set item or it has a greated distance than the final
    // item in the set. The set cursor that is used to pop() the
    // next item will be set to the lowest index of an uncheck item
    int insert(const Neighbor &nbr)
    {
        if (_size == _capacity && _data[_size - 1] < nbr)
        {
            return 0;
        }

        size_t lo = 0, hi = _size;
        while (lo < hi)
        {
            size_t mid = (lo + hi) >> 1;
            if (nbr < _data[mid])
            {
                hi = mid;
                // Make sure the same id isn't inserted into the set
            }
            else if (_data[mid].id == nbr.id)
            {
                return 0;
            }
            else
            {
                lo = mid + 1;
            }
        }

        if (lo < _capacity)
        {
            std::memmove(&_data[lo + 1], &_data[lo], (_size - lo) * sizeof(Neighbor));
        }
        _data[lo] = {nbr.id, nbr.distance};
        if (_size < _capacity)
        {
            _size++;
        }
        if (lo < _cur)
        {
            _cur = lo;
        }
        return 1;
    }

    Neighbor closest_unexpanded()
    {
        _data[_cur].expanded = true;
        size_t pre = _cur;
        while (_cur < _size && _data[_cur].expanded)
        {
            _cur++;
        }
        return _data[pre];
    }

    bool has_unexpanded_node() const
    {
        return _cur < _size;
    }

    size_t size() const
    {
        return _size;
    }

    size_t capacity() const
    {
        return _capacity;
    }

    void reserve(size_t capacity)
    {
        if (capacity + 1 > _data.size())
        {
            _data.resize(capacity + 1);
        }
        _capacity = capacity;
    }

    Neighbor &operator[](size_t i)
    {
        return _data[i];
    }

    Neighbor operator[](size_t i) const
    {
        return _data[i];
    }

    void clear()
    {
        _size = 0;
        _cur = 0;
    }

    std::vector<uint32_t> get_candidate_ids() const
    {
        std::vector<uint32_t> ids;
        ids.reserve(_size);
        for (size_t i = 0; i < _size; i++)
        {
            ids.push_back(_data[i].id);
        }
        return ids;
    }

    std::uint32_t get_candidate_id(uint32_t index) const
    {
        return (_data[index].id);
    }

    // Update the distance of the neighbor at index `idx`.
    void update_neighbor_distance_at_index(size_t idx, float new_distance)
    {
        // float totalSquared = _data[idx].distance * _data[idx].distance + new_distance * new_distance;
        // _data[idx].distance = totalSquared;
        // sqrt(totalSquared);
        _data[idx].distance += new_distance;
    }

    // Re-sort the queue so that candidates are in increasing order of distance.
    void sort_queue()
    {
        std::sort(_data.begin(), _data.begin() + _size,
                  [](const Neighbor &a, const Neighbor &b) { return a.distance < b.distance; });
    }
    
    void partition_queue(uint32_t new_size)
    {
        if (new_size < _size)
        {
            std::nth_element(_data.begin(), _data.begin() + new_size, _data.begin() + _size,
                             [](const Neighbor &a, const Neighbor &b) { return a.distance < b.distance; });
            _size = new_size;
        }
    }

    void reset_cur()
    {
        _cur = 0;
        while (_cur < _size && _data[_cur].expanded)
        {
            _cur++;
        }
    }

    void prune_queue()
    {
        // Cut the queue in half by keeping only the first half.
        size_t new_size = _size / 2;
        _data.erase(_data.begin() + new_size, _data.begin() + _size);
        _size = new_size;
    }

    void reset_size(uint32_t new_size)
    {
        _size = new_size;
    }

  private:
    size_t _size, _capacity, _cur;
    std::vector<Neighbor> _data;
};

} // namespace diskann
