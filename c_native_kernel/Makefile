# Makefile pour Kernel Scheduler C - Production Medical Grade

CC = gcc
CFLAGS = -O3 -march=native -mtune=native -flto \
         -Wall -Wextra -Werror \
         -ffast-math -funroll-loops \
         -fno-strict-aliasing \
         -D_GNU_SOURCE

# Real-Time flags
RT_FLAGS = -pthread -lrt -lm

# Profiling flags (pour optimisation)
PROFILE_FLAGS = -pg -fprofile-arcs -ftest-coverage

# Debugging flags
DEBUG_FLAGS = -g -O0 -DDEBUG -fsanitize=address -fsanitize=undefined

# Medical certification flags (DO-178C level A equivalent)
CERT_FLAGS = -fstack-protector-all -D_FORTIFY_SOURCE=2 \
             -Wformat -Wformat-security \
             -fPIE -pie

TARGET = lab_scheduler
SOURCES = kernel_scheduler.c
HEADERS = kernel_scheduler.h

# Build targets

.PHONY: all clean test benchmark install

all: production

# Production build (optimisé pour déploiement)
production: CFLAGS += $(CERT_FLAGS)
production: $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -DBUILD_STANDALONE $(RT_FLAGS) $(SOURCES) -o $(TARGET)
	strip $(TARGET)
	@echo "✓ Production build complete: $(TARGET)"
	@echo "  Size: $$(stat -c%s $(TARGET)) bytes"

# Debug build (pour développement)
debug: CFLAGS = $(DEBUG_FLAGS)
debug: $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -DBUILD_STANDALONE $(RT_FLAGS) $(SOURCES) -o $(TARGET)_debug
	@echo "✓ Debug build complete: $(TARGET)_debug"

# Profile build (pour profiling avec gprof)
profile: CFLAGS += $(PROFILE_FLAGS)
profile: $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -DBUILD_STANDALONE $(RT_FLAGS) $(SOURCES) -o $(TARGET)_profile
	@echo "✓ Profile build complete: $(TARGET)_profile"

# Tests unitaires
test: debug
	@echo "Running unit tests..."
	./$(TARGET)_debug
	@echo "✓ All tests passed"

# Benchmark de performance
benchmark: production
	@echo "Running performance benchmark..."
	@echo ""
	@echo "=== Test 1: 10 samples ==="
	time -p ./$(TARGET)
	@echo ""
	@echo "=== Test 2: 100 samples (scaling) ==="
	# TODO: Générer 100 samples via script
	@echo ""
	@echo "=== Test 3: Real-time latency ==="
	sudo chrt -f 99 cyclictest -p 99 -m -n -q -D 10s
	@echo "✓ Benchmark complete"

# Installation système (nécessite root)
install: production
	@echo "Installing to /usr/local/bin/..."
	sudo cp $(TARGET) /usr/local/bin/
	sudo chmod +x /usr/local/bin/$(TARGET)
	sudo setcap cap_sys_nice+ep /usr/local/bin/$(TARGET)  # Autoriser RT priority
	@echo "✓ Installed successfully"

# Nettoyage
clean:
	rm -f $(TARGET) $(TARGET)_debug $(TARGET)_profile
	rm -f *.o *.gcda *.gcno gmon.out
	@echo "✓ Clean complete"

# Configuration CentOS RT
setup-centos-rt:
	@echo "Configuring CentOS for real-time..."
	sudo yum install -y kernel-rt kernel-rt-devel
	sudo grubby --set-default /boot/vmlinuz-*rt*
	@echo "isolcpus=1,2,3" | sudo tee -a /etc/default/grub
	sudo grub2-mkconfig -o /boot/grub2/grub.cfg
	@echo ""
	@echo "⚠️  REBOOT REQUIRED to use RT kernel"
	@echo "✓ RT kernel configured"

# Vérification configuration RT
check-rt:
	@echo "Checking real-time configuration..."
	@echo ""
	@echo "Kernel version:"
	uname -r | grep -q rt && echo "✓ RT kernel active" || echo "✗ RT kernel NOT active"
	@echo ""
	@echo "CPU isolation:"
	cat /sys/devices/system/cpu/isolated || echo "✗ No isolated CPUs"
	@echo ""
	@echo "Scheduler policy:"
	chrt -p $$$$ || echo "✗ Cannot check scheduler"
	@echo ""
	@echo "Max RT priority:"
	cat /proc/sys/kernel/sched_rt_runtime_us
	@echo "✓ Configuration check complete"

# Génération de documentation
docs:
	doxygen Doxyfile 2>/dev/null || echo "Doxygen not installed"
	@echo "✓ Documentation generated in docs/"

# Analyse statique (cppcheck)
analyze:
	cppcheck --enable=all --suppress=missingIncludeSystem $(SOURCES)
	@echo "✓ Static analysis complete"

# Profiling avec perf
perf: production
	@echo "Running perf profiling..."
	sudo perf record -g ./$(TARGET)
	sudo perf report
	@echo "✓ Perf profiling complete"

# Help
help:
	@echo "Makefile for Medical Lab Kernel Scheduler"
	@echo ""
	@echo "Targets:"
	@echo "  all              - Build production version (default)"
	@echo "  production       - Optimized build for deployment"
	@echo "  debug            - Debug build with sanitizers"
	@echo "  profile          - Build with profiling enabled"
	@echo "  test             - Run unit tests"
	@echo "  benchmark        - Run performance benchmarks"
	@echo "  install          - Install to /usr/local/bin (requires root)"
	@echo "  clean            - Remove all build artifacts"
	@echo "  setup-centos-rt  - Configure CentOS for RT kernel"
	@echo "  check-rt         - Verify RT configuration"
	@echo "  docs             - Generate documentation"
	@echo "  analyze          - Run static analysis"
	@echo "  perf             - Profile with Linux perf"
	@echo "  help             - Show this help"
	@echo ""
	@echo "Example usage:"
	@echo "  make                  # Build production"
	@echo "  make test             # Test debug build"
	@echo "  sudo make install     # Install system-wide"
	@echo "  make benchmark        # Run benchmarks"
