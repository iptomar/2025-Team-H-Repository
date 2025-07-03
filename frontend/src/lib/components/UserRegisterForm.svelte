<script lang="ts">
	import { Button } from '$lib/components/ui/button/';
	import { Input } from '$lib/components/ui/input/';
	import { Label } from '$lib/components/ui/label/';
	import { cn } from '$lib/utils.js';
	import { auth, schools, courses } from '$lib/api';
	import { UserRole } from '$lib/types';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { isAuthenticated } from '$lib/stores/auth';

	let className: string | undefined | null = undefined;
	export { className as class };

	let isLoading = false;
	let email = '';
	let password = '';
	let confirmPassword = '';
	let selectedRole = '';
	let selectedSchool = '';
	let selectedCourse = '';
	let error = '';
	let success = '';

	let schoolsList: any[] = [];
	let coursesList: any[] = [];

	// Load schools and courses on component mount
	onMount(async () => {
		try {
			schoolsList = await schools.getAll();
			if (!schoolsList.length) {
				error = 'No schools found. Please contact admin.';
			}
			coursesList = await courses.getAll();
		} catch (err) {
			error = 'Failed to load schools.';
			console.error('Failed to load data:', err);
		}
	});

	// Load courses when school changes
	function onSchoolChange() {
		if (selectedSchool) {
			selectedCourse = ''; // Reset course selection
		}
	}

	function validateForm(): string | null {
		if (!email || !password || !confirmPassword || !selectedRole) {
			return 'Please fill in all required fields';
		}

		if (password !== confirmPassword) {
			return 'Passwords do not match';
		}

		if (password.length < 6) {
			return 'Password must be at least 6 characters long';
		}

		if (!email.includes('@')) {
			return 'Please enter a valid email address';
		}

		// Validate role-specific requirements
		if (selectedRole === UserRole.School_Timetable_Committee && !selectedSchool) {
			return 'School selection is required for School Timetable Committee role';
		}

		if (selectedRole === UserRole.Course_Timetable_Committee && !selectedCourse) {
			return 'Course selection is required for Course Timetable Committee role';
		}

		return null;
	}

	async function onSubmit() {
		isLoading = true;
		error = '';
		success = '';

		const validationError = validateForm();
		if (validationError) {
			error = validationError;
			isLoading = false;
			return;
		}

		try {
			const userData = {
				username: email,
				password: password,
				role: selectedRole as UserRole,
				school_id: selectedSchool ? parseInt(selectedSchool) : undefined,
				course_id: selectedCourse ? parseInt(selectedCourse) : undefined
			};

			const newUser = await auth.register(userData);
			
			success = 'Registration successful! Redirecting...';
			console.log('User registered:', newUser);
			// Set auth state and redirect to timetable
			isAuthenticated.set(true);
			setTimeout(() => {
				goto('/timetable');
			}, 1000);
			
		} catch (err) {
			error = err instanceof Error ? err.message : 'Registration failed';
			console.error('Registration error:', err);
		} finally {
			isLoading = false;
		}
	}

	// Get filtered courses for the selected school
	$: filteredCourses = selectedSchool 
		? coursesList.filter(course => course.school_id === parseInt(selectedSchool))
		: [];
</script>

<div class={cn('grid gap-6', className)} {...$$restProps}>
	<form on:submit|preventDefault={onSubmit}>
		<div class="grid gap-2">
			<div class="grid gap-1">
				<Label for="email">Email *</Label>
				<Input
					id="email"
					bind:value={email}
					placeholder="nome@ipt.pt"
					type="email"
					autocapitalize="none"
					autocomplete="email"
					autocorrect="off"
					disabled={isLoading}
					required
				/>
			</div>

			<div class="grid gap-1">
				<Label for="password">Password *</Label>
				<Input
					id="password"
					bind:value={password}
					placeholder="Enter password"
					type="password"
					autocomplete="new-password"
					disabled={isLoading}
					required
				/>
			</div>

			<div class="grid gap-1">
				<Label for="confirmPassword">Confirm Password *</Label>
				<Input
					id="confirmPassword"
					bind:value={confirmPassword}
					placeholder="Confirm password"
					type="password"
					autocomplete="new-password"
					disabled={isLoading}
					required
				/>
			</div>

			<div class="grid gap-1">
				<Label for="role">Role *</Label>
				<select
					id="role"
					bind:value={selectedRole}
					disabled={isLoading}
					required
					class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
				>
					<option value="">Select your role</option>
					<option value={UserRole.Administrator}>Administrator</option>
					<option value={UserRole.School_Timetable_Committee}>School Timetable Committee</option>
					<option value={UserRole.Course_Timetable_Committee}>Course Timetable Committee</option>
					<option value={UserRole.Teacher}>Teacher</option>
				</select>
			</div>

			{#if selectedRole === UserRole.School_Timetable_Committee || selectedRole === UserRole.Course_Timetable_Committee || selectedRole === UserRole.Teacher}
				<div class="grid gap-1">
					<Label for="school">School {selectedRole === UserRole.School_Timetable_Committee ? '*' : ''}</Label>
					<select
						id="school"
						bind:value={selectedSchool}
						on:change={onSchoolChange}
						disabled={isLoading}
						required={selectedRole === UserRole.School_Timetable_Committee}
						class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						<option value="">Select school</option>
						{#each schoolsList as school}
							<option value={school.school_id.toString()}>{school.name}</option>
						{/each}
					</select>
				</div>
			{/if}

			{#if selectedRole === UserRole.Course_Timetable_Committee && selectedSchool}
				<div class="grid gap-1">
					<Label for="course">Course *</Label>
					<select
						id="course"
						bind:value={selectedCourse}
						disabled={isLoading}
						required
						class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
					>
						<option value="">Select course</option>
						{#each filteredCourses as course}
							<option value={course.course_id.toString()}>{course.name}</option>
						{/each}
					</select>
				</div>
			{/if}

			{#if error}
				<div class="text-sm text-red-600 bg-red-50 p-2 rounded">
					{error}
				</div>
			{/if}

			{#if success}
				<div class="text-sm text-green-600 bg-green-50 p-2 rounded">
					{success}
				</div>
			{/if}

			<Button type="submit" disabled={isLoading || !email || !password || !confirmPassword || !selectedRole}>
				{#if isLoading}
					Registering...
				{:else}
					Register
				{/if}
			</Button>
		</div>
	</form>
</div>
